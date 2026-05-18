import requests

from datetime import date, timedelta


def get_recent_games(days_back=3):
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
        print("Error fetching games:", response.status_code)
        return {}

    return response.json()


def get_boxscore(game_pk):
    url = f"https://statsapi.mlb.com/api/v1/game/{game_pk}/boxscore"

    response = requests.get(url)

    if response.status_code != 200:
        print("Error fetching boxscore:", response.status_code)
        return {}

    return response.json()


def calculate_bullpen_usage(schedule_data):
    bullpen_stats = {}

    for date_block in schedule_data.get("dates", []):
        for game in date_block.get("games", []):

            if game["status"]["abstractGameState"] != "Final":
                continue

            game_pk = game["gamePk"]

            away_team = game["teams"]["away"]["team"]["name"]
            home_team = game["teams"]["home"]["team"]["name"]

            boxscore = get_boxscore(game_pk)

            away_pitchers = boxscore["teams"]["away"].get("pitchers", [])
            home_pitchers = boxscore["teams"]["home"].get("pitchers", [])

            away_bullpen_count = max(0, len(away_pitchers) - 1)
            home_bullpen_count = max(0, len(home_pitchers) - 1)

            if away_team not in bullpen_stats:
                bullpen_stats[away_team] = {
                    "bullpen_appearances": 0
                }

            if home_team not in bullpen_stats:
                bullpen_stats[home_team] = {
                    "bullpen_appearances": 0
                }

            bullpen_stats[away_team]["bullpen_appearances"] += away_bullpen_count
            bullpen_stats[home_team]["bullpen_appearances"] += home_bullpen_count

    return bullpen_stats

def calculate_bullpen_fatigue_score(stats):
    appearances = stats.get("bullpen_appearances", 0)

    if appearances >= 10:
        return -2.0
    elif appearances >= 7:
        return -1.0
    elif appearances <= 3:
        return 1.0
    else:
        return 0.0

if __name__ == "__main__":
    data = get_recent_games()

    bullpen_stats = calculate_bullpen_usage(data)

    for team, stats in bullpen_stats.items():
        print()
        print(team)
        print(
            f"Bullpen Appearances: "
            f"{stats['bullpen_appearances']}"
        )
        fatigue_score = calculate_bullpen_fatigue_score(stats)
        print(f"Bullpen Fatigue Score: {fatigue_score:+.1f}")