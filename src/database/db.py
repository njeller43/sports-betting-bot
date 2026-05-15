import sqlite3

DB_PATH = "data/betting_data.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS collection_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS betting_odds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            sport TEXT NOT NULL,
            event TEXT NOT NULL,
            sportsbook TEXT NOT NULL,
            team TEXT NOT NULL,
            odds INTEGER NOT NULL,
            implied_probability REAL NOT NULL,
            collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (run_id) REFERENCES collection_runs(id)
        )
    ''')

    connection.commit()
    connection.close()

def create_collection_run():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute('INSERT INTO collection_runs DEFAULT VALUES')
    run_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return run_id

def insert_betting_odds(betting_objects, run_id):
    connection = get_connection()
    cursor = connection.cursor()

    for bet in betting_objects:
        cursor.execute('''
            INSERT INTO betting_odds (run_id, sport, event, sportsbook, team, odds, implied_probability)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            run_id,
            bet['sport'],
            bet['event'],
            bet['sportsbook'],
            bet['team'],
            bet['odds'],
            bet['implied_probability']
        ))

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