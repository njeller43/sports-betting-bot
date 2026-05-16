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


def get_pitcher_stats(pitcher_id):

    if pitcher_id is None:
        return {}

    url = f"https://statsapi.mlb.com/api/v1/people/{pitcher_id}"

    params = {
        "hydrate": "stats(group=[pitching],type=[season])"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Error fetching pitcher stats:", response.status_code)
        return {}

    data = response.json()

    people = data.get("people", [])

    if not people:
        return {}

    stats = (
        people[0]
        .get("stats", [{}])[0]
        .get("splits", [{}])[0]
        .get("stat", {})
    )

    return {
        "era": stats.get("era"),
        "whip": stats.get("whip"),
        "strikeouts": stats.get("strikeOuts"),
        "wins": stats.get("wins"),
        "losses": stats.get("losses"),
    }

def calculate_pitcher_score(stats):
    if not stats:
        return 0

    era = float(stats.get("era") or 0)
    whip = float(stats.get("whip") or 0)
    strikeouts = int(stats.get("strikeouts") or 0)

    score = 0

    if era > 0:
        score += max(0, 5 - era)

    if whip > 0:
        score += max(0, 2 - whip)

    score += strikeouts / 50

    return round(score, 2)

if __name__ == "__main__":
    data = get_today_pitchers()

    for date in data.get("dates", []):
        print("Date:", date.get("date"))

        for game in date.get("games", []):

            away_team = game["teams"]["away"]["team"]["name"]
            home_team = game["teams"]["home"]["team"]["name"]

            away_pitcher_data = (
                game["teams"]["away"]
                .get("probablePitcher", {})
            )

            home_pitcher_data = (
                game["teams"]["home"]
                .get("probablePitcher", {})
            )

            away_pitcher = away_pitcher_data.get("fullName", "TBD")
            home_pitcher = home_pitcher_data.get("fullName", "TBD")

            away_pitcher_id = away_pitcher_data.get("id")
            home_pitcher_id = home_pitcher_data.get("id")

            away_stats = get_pitcher_stats(away_pitcher_id)
            home_stats = get_pitcher_stats(home_pitcher_id)

            away_pitcher_score = calculate_pitcher_score(away_stats)
            home_pitcher_score = calculate_pitcher_score(home_stats)

            print()
            print("=" * 60)
            print(f"{away_team} at {home_team}")
            print("=" * 60)

            print()
            print(f"Away Pitcher: {away_pitcher}")
            print(away_stats)
            print(f"Pitcher Score: {away_pitcher_score}")

            print()
            print(f"Home Pitcher: {home_pitcher}")
            print(home_stats)
            print(f"Pitcher Score: {home_pitcher_score}")