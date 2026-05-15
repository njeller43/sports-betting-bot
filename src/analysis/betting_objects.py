def create_betting_object(
        sport,
        event_name,
        sportsbook,
        team,
        odds,
        implied_probability
):
    return {
        "sport": sport,
        "event": event_name,
        "sportsbook": sportsbook,
        "team": team,
        "odds": odds,
        "implied_probability": implied_probability
    }