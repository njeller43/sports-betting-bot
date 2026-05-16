from src.database.schema import get_connection, create_schema


def get_or_create_sportsbook(name):
    create_schema()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO sportsbooks (name)
        VALUES (?)
    """, (name,))

    cursor.execute("""
        SELECT id
        FROM sportsbooks
        WHERE name = ?
    """, (name,))

    sportsbook_id = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return sportsbook_id


def get_or_create_game(
    external_event_id,
    sport,
    home_team,
    away_team,
    commence_time
):
    create_schema()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM games
        WHERE external_event_id = ?
    """, (external_event_id,))

    existing = cursor.fetchone()

    if existing:
        conn.close()
        return existing[0]

    cursor.execute("""
        INSERT INTO games (
            external_event_id,
            sport,
            home_team,
            away_team,
            commence_time
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        external_event_id,
        sport,
        home_team,
        away_team,
        commence_time
    ))

    game_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return game_id


if __name__ == "__main__":
    sportsbook_id = get_or_create_sportsbook("FanDuel")

    game_id = get_or_create_game(
        external_event_id="test_event_1",
        sport="baseball_mlb",
        home_team="Test Home",
        away_team="Test Away",
        commence_time="2026-05-16T12:00:00Z"
    )

    print(f"Sportsbook ID: {sportsbook_id}")
    print(f"Game ID: {game_id}")