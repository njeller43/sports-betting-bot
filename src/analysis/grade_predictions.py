import sqlite3

from src.collectors.mlb_stats_collector import get_recent_games


def get_saved_edge_reports():
    conn = sqlite3.connect("sports_betting.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            event,
            team,
            odds
        FROM edge_reports
        WHERE prediction_correct IS NULL
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


def build_winner_lookup():
    recent_games = get_recent_games()

    winners = {}

    for date in recent_games.get("dates", []):
        for game in date.get("games", []):

            if game["status"]["abstractGameState"] != "Final":
                continue

            away = game["teams"]["away"]
            home = game["teams"]["home"]

            away_team = away["team"]["name"]
            home_team = home["team"]["name"]

            away_score = away.get("score")
            home_score = home.get("score")

            if away_score is None or home_score is None:
                continue

            if away_score > home_score:
                winner = away_team
            elif home_score > away_score:
                winner = home_team
            else:
                continue

            event_name = f"{away_team} vs {home_team}"
            winners[event_name] = winner

    return winners


def calculate_profit(odds, won):

    if not won:
        return -100

    if odds > 0:
        return odds

    return (100 / abs(odds)) * 100


def grade_predictions():

    reports = get_saved_edge_reports()

    winners = build_winner_lookup()

    conn = sqlite3.connect("sports_betting.db")
    cursor = conn.cursor()

    for report in reports:

        report_id, event, predicted_team, odds = report

        if event not in winners:
            continue

        actual_winner = winners[event]

        correct = predicted_team == actual_winner

        profit_loss = calculate_profit(odds, correct)

        cursor.execute("""
            UPDATE edge_reports
            SET
                actual_winner = ?,
                prediction_correct = ?,
                profit_loss = ?
            WHERE id = ?
        """, (
            actual_winner,
            int(correct),
            profit_loss,
            report_id
        ))

        print()
        print(event)
        print(f"Predicted: {predicted_team}")
        print(f"Actual Winner: {actual_winner}")
        print(f"Correct: {correct}")
        print(f"Profit/Loss: {profit_loss:+.2f}")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    grade_predictions()