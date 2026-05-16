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

def save_odds_snapshot(
    external_event_id,
    sport,
    home_team,
    away_team,
    commence_time,
    sportsbook_name,
    team,
    market,
    odds,
    implied_probability
):
    game_id = get_or_create_game(
        external_event_id=external_event_id,
        sport=sport,
        home_team=home_team,
        away_team=away_team,
        commence_time=commence_time
    )

    sportsbook_id = get_or_create_sportsbook(sportsbook_name)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO odds_snapshots (
            game_id,
            sportsbook_id,
            team,
            market,
            odds,
            implied_probability
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        game_id,
        sportsbook_id,
        team,
        market,
        odds,
        implied_probability
    ))

    conn.commit()
    conn.close()

def save_model_prediction(
    external_event_id,
    sport,
    home_team,
    away_team,
    commence_time,
    team,
    sportsbook,
    odds,
    trend_score,
    pitcher_score,
    edge_score,
    signal,
    model_win_probability=None,
    fair_odds=None
):
    game_id = get_or_create_game(
        external_event_id=external_event_id,
        sport=sport,
        home_team=home_team,
        away_team=away_team,
        commence_time=commence_time
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO model_predictions (
            game_id,
            team,
            sportsbook,
            odds,
            trend_score,
            pitcher_score,
            edge_score,
            signal,
            model_win_probability,
            fair_odds
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        game_id,
        team,
        sportsbook,
        odds,
        trend_score,
        pitcher_score,
        edge_score,
        signal,
        model_win_probability,
        fair_odds
    ))

    conn.commit()
    conn.close()

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

