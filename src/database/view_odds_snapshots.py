from src.database.schema import get_connection


def view_recent_odds(limit=20):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            g.sport,
            g.away_team,
            g.home_team,
            g.commence_time,
            s.name,
            o.team,
            o.market,
            o.odds,
            o.implied_probability,
            o.collected_at
        FROM odds_snapshots o
        JOIN games g ON o.game_id = g.id
        JOIN sportsbooks s ON o.sportsbook_id = s.id
        ORDER BY o.collected_at DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        print(row)


if __name__ == "__main__":
    view_recent_odds()