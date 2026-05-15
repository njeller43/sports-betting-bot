def create_betting_object(
        event_name,
        sportsbook,
        team,
        odds,
        implied_probability
):
    return {
        "event": event_name,
        "sportsbook": sportsbook,
        "team": team,
        "odds": odds,
        "implied_probability": implied_probability
    }