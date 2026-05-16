def is_better_odds(new_odds, current_odds):
    if new_odds < 0 and current_odds < 0:
        return new_odds > current_odds

    if new_odds > 0 and current_odds > 0:
        return new_odds > current_odds

    return new_odds > current_odds

    return False

def calculate_recent_bonus(results):
    recent_results = results[-3:]

    recent_bonus = 0

    for result in recent_results:
        if result == "W":
            recent_bonus += 0.5
        else:
            recent_bonus -= 0.5

    return recent_bonus


def calculate_edge_score(
    trend_score,
    odds,
    pitcher_score,
    recent_bonus,
):
    return (
        trend_score
        + recent_bonus
        + (odds / 100)
        + pitcher_score
    )


def classify_signal(edge_score):
    if edge_score >= 2:
        return "Potential Value Bet"

    elif edge_score <= -2:
        return "Avoid / Cold Team"

    return "Neutral"

def estimate_win_probability(edge_score):

    probability = 50 + (edge_score * 3)
    probability = max(0, min(99, probability))

    return round(probability, 2)