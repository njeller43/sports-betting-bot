import requests


def get_mlb_schedule():
    url = "https://statsapi.mlb.com/api/v1/schedule"

    params = {
        "sportId": 1
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Error fetching MLB schedule:", response.status_code)
        return {}

    return response.json()


if __name__ == "__main__":
    data = get_mlb_schedule()

    dates = data.get("dates", [])

    for date in dates:
        print("Date:", date.get("date"))

        for game in date.get("games", []):
            away_team = game["teams"]["away"]["team"]["name"]
            home_team = game["teams"]["home"]["team"]["name"]
            status = game["status"]["detailedState"]

            print(f"{away_team} at {home_team} — {status}")