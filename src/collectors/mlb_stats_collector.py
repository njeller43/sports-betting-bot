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


if __name__ == "__main__":
    data = get_recent_games()

    dates = data.get("dates", [])

    for date in dates:
        print("Date:", date.get("date"))

        for game in date.get("games", []):
            away_team = game["teams"]["away"]["team"]["name"]
            home_team = game["teams"]["home"]["team"]["name"]
            status = game["status"]["abstractGameState"]

            if status != "Final":
                continue
            away_score = game["teams"]["away"].get("score")
            home_score = game["teams"]["home"].get("score")

            print(f"{away_team} {away_score} at {home_team} {home_score}")
