from src.database.schema import get_connection


def view_recent_predictions(limit=20):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            g.sport,
            g.away_team,
            g.home_team,
            g.commence_time,
            p.team,
            p.sportsbook,
            p.odds,
            p.trend_score,
            p.pitcher_score,
            p.edge_score,
            p.signal,
            p.created_at
        FROM model_predictions p
        JOIN games g ON p.game_id = g.id
        ORDER BY p.created_at DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        print(row)


if __name__ == "__main__":
    view_recent_predictions()