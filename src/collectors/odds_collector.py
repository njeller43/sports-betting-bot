import os
import requests

from dotenv import load_dotenv
from src.analysis.implied_probability import american_odds_to_probability
from src.analysis.betting_objects import create_betting_object

load_dotenv()

API_KEY = os.getenv("ODDS_API_KEY")

def get_odds_data(sport="americanfootball_nfl"):
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"

    params = {
    "apiKey": API_KEY,
    "regions": "us",
    "markets": "h2h",
    "oddsFormat": "american"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Error fetching odds data:", response.status_code, response.text)
        return []

    return response.json()

def display_odds(events):

    for event in events:

        print()
        print("=" * 60)
        print(f"{event['home_team']} vs {event['away_team']}")
        print("=" * 60)

        for bookmaker in event['bookmakers']:
            print()
            print(f"Sportsbook: {bookmaker['title']}")

            for market in bookmaker['markets']:

                print(f" Market: {market['key']}")

                for outcome in market['outcomes']:
                    probability = american_odds_to_probability(outcome['price'])
                    betting_object = create_betting_object(
                        event_name=f"{event['home_team']} vs {event['away_team']}",
                        sportsbook=bookmaker['title'],
                        team=outcome['name'],
                        odds=outcome['price'],
                        implied_probability=probability
                    )
                    print(betting_object)

if __name__ == "__main__":
    odds_data = get_odds_data()
    display_odds(odds_data)

