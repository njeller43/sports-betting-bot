from src.analysis.implied_probability import american_odds_to_probability


def calculate_market_edge(model_win_probability, sportsbook_odds):
    sportsbook_probability = american_odds_to_probability(sportsbook_odds) * 100

    edge_percentage = model_win_probability - sportsbook_probability

    return round(edge_percentage, 2)


def probability_to_american_odds(probability):
    """
    Convert model win probability into fair American odds.
    Probability should be entered as a percentage, like 62.5.
    """

    if probability <= 0 or probability >= 100:
        return None

    probability_decimal = probability / 100

    if probability_decimal >= 0.5:
        odds = -((probability_decimal / (1 - probability_decimal)) * 100)
    else:
        odds = ((1 - probability_decimal) / probability_decimal) * 100

    return round(odds)


if __name__ == "__main__":
    model_probability = 62.5
    sportsbook_odds = -120

    edge = calculate_market_edge(
        model_probability,
        sportsbook_odds
    )

    fair_odds = probability_to_american_odds(
        model_probability
    )

    print(f"Model Win Probability: {model_probability}%")
    print(f"Sportsbook Odds: {sportsbook_odds}")
    print(f"Fair Odds: {fair_odds}")
    print(f"Estimated Edge: {edge:+.2f}%")