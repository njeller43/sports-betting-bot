from src.database.schema import get_connection


def get_line_movement_report():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            g.away_team,
            g.home_team,
            g.commence_time,
            s.name AS sportsbook,
            o.team,
            o.market,
            o.odds,
            o.collected_at
        FROM odds_snapshots o
        JOIN games g ON o.game_id = g.id
        JOIN sportsbooks s ON o.sportsbook_id = s.id
        WHERE o.market = 'h2h'
        ORDER BY
            g.commence_time,
            s.name,
            o.team,
            o.collected_at
    """)

    rows = cursor.fetchall()
    conn.close()

    grouped = {}

    for row in rows:
        (
            away_team,
            home_team,
            commence_time,
            sportsbook,
            team,
            market,
            odds,
            collected_at,
        ) = row

        key = (
            away_team,
            home_team,
            commence_time,
            sportsbook,
            team,
        )

        if key not in grouped:
            grouped[key] = []

        grouped[key].append({
            "odds": odds,
            "collected_at": collected_at,
        })

    reports = []

    for key, history in grouped.items():
        if len(history) < 2:
            continue

        first = history[0]
        latest = history[-1]

        opening_odds = first["odds"]
        latest_odds = latest["odds"]

        movement = latest_odds - opening_odds

        if movement == 0:
            continue

        (
            away_team,
            home_team,
            commence_time,
            sportsbook,
            team,
        ) = key

        reports.append({
            "event": f"{away_team} vs {home_team}",
            "commence_time": commence_time,
            "sportsbook": sportsbook,
            "team": team,
            "opening_odds": opening_odds,
            "latest_odds": latest_odds,
            "movement": movement,
            "first_seen": first["collected_at"],
            "last_seen": latest["collected_at"],
        })

    reports.sort(
        key=lambda report: abs(report["movement"]),
        reverse=True
    )

    return reports


if __name__ == "__main__":
    reports = get_line_movement_report()

    print()
    print("=" * 60)
    print("LINE MOVEMENT REPORT")
    print("=" * 60)

    if not reports:
        print("No line movement detected yet.")
        print("Run the odds collector multiple times over time.")
    else:
        for report in reports[:25]:
            print()
            print(report["event"])
            print(f"Team: {report['team']}")
            print(f"Sportsbook: {report['sportsbook']}")
            print(f"Opening Odds: {report['opening_odds']}")
            print(f"Latest Odds: {report['latest_odds']}")
            print(f"Movement: {report['movement']:+}")
            print(f"First Seen: {report['first_seen']}")
            print(f"Last Seen: {report['last_seen']}")