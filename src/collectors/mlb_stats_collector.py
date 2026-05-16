import requests


def get_recent_games(days_back=10):
    url = "https://statsapi.mlb.com/api/v1/schedule"

    params = {
        "sportId": 1,
        "startDate": "2026-05-05",
        "endDate": "2026-05-15"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Error fetching MLB games:", response.status_code)
        return {}

    return response.json()

def calculate_streak(results):
    if not results:
        return "N/A"

    latest = results[-1]
    streak = 0

    for result in reversed(results):
        if result == latest:
            streak += 1
        else:
            break
    return f"{latest} {streak}"

def calculate_team_trends(data):
    team_stats = {}

    for date in data.get("dates", []):
        for game in date.get("games", []):
            if game["status"]["abstractGameState"] != "Final":
                continue

            away = game["teams"]["away"]
            home = game["teams"]["home"]

            away_score = away.get("score")
            home_score = home.get("score")

            if away_score is None or home_score is None:
                continue

            away_team = away["team"]["name"]
            home_team = home["team"]["name"]

            for team in [away_team, home_team]:
                if team not in team_stats:
                    team_stats[team] = {
                        "wins": 0,
                        "losses": 0,
                        "runs_scored": 0,
                        "runs_allowed": 0,
                        "results": []
                    }

            if away_score > home_score:
                away_result = "W"
                home_result = "L"
            else:
                away_result = "L"
                home_result = "W"

            team_stats[away_team]["runs_scored"] += away_score
            team_stats[away_team]["runs_allowed"] += home_score
            team_stats[away_team]["results"].append(away_result)

            team_stats[home_team]["runs_scored"] += home_score
            team_stats[home_team]["runs_allowed"] += away_score
            team_stats[home_team]["results"].append(home_result)

            if away_result == "W":
                team_stats[away_team]["wins"] += 1
                team_stats[home_team]["losses"] += 1
            else:
                team_stats[away_team]["losses"] += 1
                team_stats[home_team]["wins"] += 1

    return team_stats

if __name__ == "__main__":
    data = get_recent_games()
    trends = calculate_team_trends(data)

    for team, stats in trends.items():
        run_diff = stats["runs_scored"] - stats["runs_allowed"]

        print()
        print(team)
        print(f"Record: {stats['wins']}-{stats['losses']}")
        print(f"Runs Scored: {stats['runs_scored']}")
        print(f"Runs Allowed: {stats['runs_allowed']}")
        print(f"Run Differential: {run_diff:+}")
        streak = calculate_streak(stats["results"])
        print(f"Current Streak: {streak}")
        print(f"Results: {' '.join(stats['results'])}")
