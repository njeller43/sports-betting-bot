import sqlite3

DB_PATH = "data/betting_data.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS betting_odds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT NOT NULL,
            sportsbook TEXT NOT NULL,
            team TEXT NOT NULL,
            odds INTEGER NOT NULL,
            implied_probability REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully.")