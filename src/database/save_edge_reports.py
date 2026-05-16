import sqlite3


def save_edge_report(report):

    conn = sqlite3.connect("sports_betting.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS edge_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT,
            team TEXT,
            sportsbook TEXT,
            odds INTEGER,
            line_difference INTEGER,
            trend_score REAL,
            edge_score REAL,
            streak TEXT,
            signal TEXT,
            actual_winner TEXT,
            prediction_correct INTEGER,
            profit_loss REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        INSERT INTO edge_reports (
            event,
            team,
            sportsbook,
            odds,
            line_difference,
            trend_score,
            edge_score,
            streak,
            signal
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        report["event"],
        report["team"],
        report["sportsbook"],
        report["odds"],
        report["line_difference"],
        report["trend_score"],
        report["edge_score"],
        report["streak"],
        report["signal"]
    ))

    conn.commit()
    conn.close()