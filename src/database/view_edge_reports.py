import sqlite3


def view_recent_edge_reports(limit=20):
    conn = sqlite3.connect("sports_betting.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            event,
            team,
            sportsbook,
            odds,
            line_difference,
            trend_score,
            edge_score,
            streak,
            signal,
            created_at
        FROM edge_reports
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        print(row)


if __name__ == "__main__":
    view_recent_edge_reports()