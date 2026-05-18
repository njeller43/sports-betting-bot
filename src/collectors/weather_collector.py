import requests


TEAM_LOCATIONS = {
    "New York Yankees": "Bronx,NY",
    "New York Mets": "Queens,NY",
    "Boston Red Sox": "Boston,MA",
    "Philadelphia Phillies": "Philadelphia,PA",
    "Baltimore Orioles": "Baltimore,MD",
    "Washington Nationals": "Washington,DC",
    "Chicago Cubs": "Chicago,IL",
    "Chicago White Sox": "Chicago,IL",
    "Cincinnati Reds": "Cincinnati,OH",
    "Cleveland Guardians": "Cleveland,OH",
    "Colorado Rockies": "Denver,CO",
    "Arizona Diamondbacks": "Phoenix,AZ",
    "Texas Rangers": "Arlington,TX",
    "Houston Astros": "Houston,TX",
    "Seattle Mariners": "Seattle,WA",
    "San Diego Padres": "San Diego,CA",
    "Los Angeles Dodgers": "Los Angeles,CA",
    "Los Angeles Angels": "Anaheim,CA",
    "San Francisco Giants": "San Francisco,CA",
    "Oakland Athletics": "Oakland,CA",
    "Athletics": "Sacramento,CA",
    "Tampa Bay Rays": "St. Petersburg,FL",
    "Miami Marlins": "Miami,FL",
    "Milwaukee Brewers": "Milwaukee,WI",
    "Minnesota Twins": "Minneapolis,MN",
    "Atlanta Braves": "Atlanta,GA",
    "Pittsburgh Pirates": "Pittsburgh,PA",
    "Kansas City Royals": "Kansas City,MO",
    "St. Louis Cardinals": "St. Louis,MO",
    "Toronto Blue Jays": "Toronto,ON",
    "Detroit Tigers": "Detroit,MI",
}


def get_weather(home_team):
    location = TEAM_LOCATIONS.get(home_team)

    if not location:
        return {
            "temperature": 70,
            "wind_speed": 5,
        }

    url = f"https://wttr.in/{location}?format=j1"

    response = requests.get(url)

    if response.status_code != 200:
        return {
            "temperature": 70,
            "wind_speed": 5,
        }

    data = response.json()
    current = data["current_condition"][0]

    return {
        "temperature": int(current["temp_F"]),
        "wind_speed": int(current["windspeedMiles"]),
    }


def calculate_weather_bonus(weather):
    temperature = weather["temperature"]
    wind_speed = weather["wind_speed"]

    temp_bonus = 0
    wind_bonus = 0

    if temperature >= 85:
        temp_bonus += 1.0
    elif temperature <= 45:
        temp_bonus -= 1.0

    if wind_speed >= 15:
        wind_bonus += 0.5

    return round(temp_bonus + wind_bonus, 2)


if __name__ == "__main__":
    weather = get_weather("Philadelphia Phillies")
    print(weather)

    bonus = calculate_weather_bonus(weather)
    print(f"Weather Bonus: {bonus:+.2f}")