import requests

from datetime import date, timedelta

def get_recent_games(days_back=10):
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

def calculate_recent_offense(recent_runs):
    if not recent_runs:
        return 0

    recent_3 = recent_runs[-3:]
    recent_5 = recent_runs[-5:]

    average_3 = sum(recent_3) / len(recent_3)
    average_5 = sum(recent_5) / len(recent_5)

    weighted_Average = (average_3 * 0.6) + (average_5 * 0.4
    )

    return round(weighted_Average, 2)

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
                        "results": [],
                        "recent_runs": [],

                        "home_wins": 0,
                        "home_losses": 0,
                        "away_wins": 0,
                        "away_losses": 0,

                        "home_runs_scored": 0,
                        "home_runs_allowed": 0,

                        "away_runs_scored": 0,
                        "away_runs_allowed": 0,
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
            team_stats[away_team]["recent_runs"].append(away_score)

            team_stats[home_team]["runs_scored"] += home_score
            team_stats[home_team]["runs_allowed"] += away_score
            team_stats[home_team]["results"].append(home_result)
            team_stats[home_team]["recent_runs"].append(home_score)

            team_stats[away_team]["away_runs_scored"] += away_score
            team_stats[away_team]["away_runs_allowed"] += home_score

            team_stats[home_team]["home_runs_scored"] += home_score
            team_stats[home_team]["home_runs_allowed"] += away_score

            if away_result == "W":
                team_stats[away_team]["wins"] += 1
                team_stats[home_team]["losses"] += 1
                team_stats[away_team]["away_wins"] += 1
                team_stats[home_team]["home_losses"] += 1
            else:
                team_stats[away_team]["losses"] += 1
                team_stats[home_team]["wins"] += 1
                team_stats[away_team]["away_losses"] += 1
                team_stats[home_team]["home_wins"] += 1

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
        print(f"Home Record: {stats['home_wins']}-{stats['home_losses']}")
        print(f"Away Record: {stats['away_wins']}-{stats['away_losses']}")
        streak = calculate_streak(stats["results"])
        print(f"Current Streak: {streak}")
        print(f"Results: {' '.join(stats['results'])}")
