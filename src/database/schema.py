import sqlite3


DB_PATH = "data/sports_betting_warehouse.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_schema():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            external_event_id TEXT,
            sport TEXT NOT NULL,
            home_team TEXT NOT NULL,
            away_team TEXT NOT NULL,
            commence_time TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sportsbooks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS odds_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL,
            sportsbook_id INTEGER NOT NULL,
            team TEXT NOT NULL,
            market TEXT NOT NULL,
            odds INTEGER NOT NULL,
            implied_probability REAL,
            collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (game_id) REFERENCES games(id),
            FOREIGN KEY (sportsbook_id) REFERENCES sportsbooks(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS team_trends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team TEXT NOT NULL,
            sport TEXT NOT NULL,
            wins INTEGER,
            losses INTEGER,
            runs_scored INTEGER,
            runs_allowed INTEGER,
            run_differential INTEGER,
            streak TEXT,
            collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pitcher_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pitcher_id INTEGER,
            pitcher_name TEXT,
            team TEXT,
            era REAL,
            whip REAL,
            strikeouts INTEGER,
            wins INTEGER,
            losses INTEGER,
            pitcher_score REAL,
            collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS model_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER,
            commence_time TEXT,
            team TEXT NOT NULL,
            sportsbook TEXT,
            odds INTEGER,
            trend_score REAL,
            pitcher_score REAL,
            edge_score REAL,
            signal TEXT,
            model_win_probability REAL,
            fair_odds INTEGER,
            market_edge REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (game_id) REFERENCES games(id)
            
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS graded_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prediction_id INTEGER NOT NULL,
            actual_winner TEXT,
            prediction_correct INTEGER,
            profit_loss REAL,
            graded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (prediction_id) REFERENCES model_predictions(id)
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_schema()
    print("Sports betting warehouse schema created successfully.")