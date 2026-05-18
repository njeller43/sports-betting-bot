PARK_FACTORS = {
    "Colorado Rockies": 1.25,
    "Boston Red Sox": 1.10,
    "Cincinnati Reds": 1.08,
    "Philadelphia Phillies": 1.06,
    "Baltimore Orioles": 1.04,
    "Chicago White Sox": 1.03,
    "Texas Rangers": 1.03,
    "Arizona Diamondbacks": 1.02,

    "San Diego Padres": 0.95,
    "Seattle Mariners": 0.94,
    "Tampa Bay Rays": 0.94,
    "Miami Marlins": 0.93,
    "San Francisco Giants": 0.92,
    "Oakland Athletics": 0.91,
}


def get_park_factor(home_team):
    return PARK_FACTORS.get(home_team, 1.00)


def calculate_park_factor_bonus(home_team):
    park_factor = get_park_factor(home_team)

    bonus = (park_factor - 1.00) * 10

    return round(bonus, 2)