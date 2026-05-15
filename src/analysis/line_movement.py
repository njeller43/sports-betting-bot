from src.database.db import fetch_all_betting_odds

def analyze_line_movement():
    rows = fetch_all_betting_odds()

    print(f"Total rows fetched: {len(rows)}")

    if len(rows) < 2:
        print("Not enough data to analyze movement yet.")
        return

    latest_by_team = {}

    for row in rows:
        run_id = row[1]
        event = row[2]
        sportsbook = row[3]
        team = row[4]
        odds = row[5]

        key = (event, sportsbook, team)

        if key not in latest_by_team:
            latest_by_team[key] = []

        latest_by_team[key].append((run_id, odds))

    print()
    print("LINE MOVEMENT REPORT")
    print("=" * 60)

    for key, history in latest_by_team.items():
        history.sort(key=lambda x: x[0])

        if len(history) >= 2:
            previous_odds = history[-2][1]
            latest_odds = history[-1][1]

            if previous_odds != latest_odds:
                event, sportsbook, team = key

                print()
                print(f"{event}")
                print(f"Team: {team}")
                print(f"Sportsbook: {sportsbook}")
                print(f"Opening Odds: {previous_odds}")
                print(f"Latest Odds: {latest_odds}")

if __name__ == "__main__":
    analyze_line_movement()