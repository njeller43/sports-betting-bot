import requests


def get_today_pitchers():
    url = "https://statsapi.mlb.com/api/v1/schedule"

    params = {
        "sportId": 1,
        "hydrate": "probablePitcher"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Error fetching pitcher data:", response.status_code)
        return {}

    return response.json()


if __name__ == "__main__":
    data = get_today_pitchers()

    for date in data.get("dates", []):
        print("Date:", date.get("date"))

        for game in date.get("games", []):
            away_team = game["teams"]["away"]["team"]["name"]
            home_team = game["teams"]["home"]["team"]["name"]

            away_pitcher = game["teams"]["away"].get("probablePitcher", {}).get("fullName", "TBD")
            home_pitcher = game["teams"]["home"].get("probablePitcher", {}).get("fullName", "TBD")

            print()
            print(f"{away_team} at {home_team}")
            print(f"Away Pitcher: {away_pitcher}")
            print(f"Home Pitcher: {home_pitcher}")