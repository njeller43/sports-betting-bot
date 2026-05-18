import requests

from datetime import date, timedelta
from datetime import datetime, timezone
from src.database.schema import get_connection


def get_recent_completed_games(days_back=3):

    url = "https://statsapi.mlb.com/api/v1/schedule"

    end_date = date.today()
    start_date = end_date - timedelta(days=days_back)

    params = {
        "sportId": 1,
        "startDate": start_date.strftime("%Y-%m-%d"),
        "endDate": end_date.strftime("%Y-%m-%d"),
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Error fetching results.")
        return []

    return response.json()


def extract_completed_games(data):

    completed_games = []

    for date_block in data.get("dates", []):
        for game in date_block.get("games", []):

            if game["status"]["abstractGameState"] != "Final":
                continue

            home_team = game["teams"]["home"]["team"]["name"]
            away_team = game["teams"]["away"]["team"]["name"]

            home_score = game["teams"]["home"]["score"]
            away_score = game["teams"]["away"]["score"]

            winner = (
                home_team
                if home_score > away_score
                else away_team
            )

            completed_games.append({
                "event_id": game["gamePk"],
                "home_team": home_team,
                "away_team": away_team,
                "winner": winner,
                "home_score": home_score,
                "away_score": away_score,
            })

    return completed_games


def get_ungraded_predictions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            mp.id,
            mp.commence_time,
            g.home_team,
            g.away_team,
            mp.team,
            mp.odds,
            mp.signal
        FROM model_predictions mp
        JOIN games g
            ON mp.game_id = g.id
        LEFT JOIN graded_results gr
            ON mp.id = gr.prediction_id
        WHERE gr.id IS NULL
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def calculate_profit(odds):

    if odds > 0:
        return odds / 100

    return 100 / abs(odds)


def grade_predictions(completed_games):

    predictions = get_ungraded_predictions()

    print(f"Completed Games Found: {len(completed_games)}")
    print(f"Ungraded Predictions Found: {len(predictions)}")

    conn = get_connection()
    cursor = conn.cursor()

    total_predictions = 0
    correct_predictions = 0
    total_profit = 0

    for prediction in predictions:

        (
            prediction_id,
            commence_time,
            home_team,
            away_team,
            predicted_team,
            odds,
            signal,
        ) = prediction

        prediction_time = datetime.fromisoformat(commence_time.replace("Z", "+00:00"))
        if prediction_time > datetime.now(timezone.utc):
            continue

        matching_game = None

        for game in completed_games:

            if (
                game["home_team"] == home_team
                and game["away_team"] == away_team
            ):
                matching_game = game
                break

        if not matching_game:
            print(f"No matching game found")
            print(f"Prediction: {away_team} vs {home_team}")

            continue

        total_predictions += 1

        correct = (
            predicted_team
            == matching_game["winner"]
        )

        if correct:
            correct_predictions += 1
            profit_loss = calculate_profit(odds)
            total_profit += profit_loss
        else:
            profit_loss = -1
            total_profit -= 1

        cursor.execute("""
            INSERT INTO graded_results (
                prediction_id,
                actual_winner,
                prediction_correct,
                profit_loss
            )
            VALUES (?, ?, ?, ?)
        """, (
            prediction_id,
            matching_game["winner"],
            int(correct),
            round(profit_loss, 2),
        ))

    conn.commit()
    conn.close()

    print()
    print("=" * 60)
    print("BACKTEST RESULTS")
    print("=" * 60)

    print(f"Predictions Graded: {total_predictions}")
    print(f"Correct Predictions: {correct_predictions}")

    if total_predictions > 0:
        accuracy = (
            correct_predictions
            / total_predictions
        ) * 100

        print(f"Accuracy: {accuracy:.2f}%")

    print(f"Total Units: {total_profit:+.2f}")


if __name__ == "__main__":

    data = get_recent_completed_games()

    completed_games = extract_completed_games(data)

    grade_predictions(completed_games)