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

def insert_betting_odds(betting_objects):
    connection = get_connection()
    cursor = connection.cursor()

    for bet in betting_objects:
        cursor.execute('''
            INSERT INTO betting_odds (event, sportsbook, team, odds, implied_probability)
            VALUES (?, ?, ?, ?, ?)
        ''', (bet['event'], bet['sportsbook'], bet['team'], bet['odds'], bet['implied_probability']))

    connection.commit()
    connection.close()

def fetch_all_betting_odds():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM betting_odds')
    rows = cursor.fetchall()

    connection.close()
    return rows

if __name__ == "__main__":
    rows = fetch_all_betting_odds()
    for row in rows[:10]:
        print(row)
    print()
    print(f"Total Rows: {len(rows)}")