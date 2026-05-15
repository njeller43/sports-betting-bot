def american_odds_to_probability(odds):
    """Convert American odds to implied probability.
    
       Example:
       -135 means risk $135 to win $100.
       +150 means risk $100 to win $150."""
    
    if odds < 0:
        return abs(odds) / (abs(odds) + 100)
    return 100 / (odds + 100)

if __name__ == "__main__":
    test_odds = [-135, 114, -425, 330]

    for odds in test_odds:
        probability = american_odds_to_probability(odds)
        print(f"Odds: {odds}, Implied Probability: {probability:.2%}")
        