import os
import requests

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ODDS_API_KEY")

SPORT = "americanfootball_nfl"

url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds"

params = {
    "apiKey": API_KEY,
    "regions": "us",
    "markets": "h2h",
    "oddsFormat": "american"
}

response = requests.get(url, params=params)

data = response.json()

print("Status Code:", response.status_code)
print() 

for event in data:
    print("Event:", event['home_team'], "vs", event['away_team'])
    for bookmaker in event['bookmakers']:
        print("  Bookmaker:", bookmaker['title'])
        for market in bookmaker['markets']:
            print("    Market:", market['key'])
            for outcome in market['outcomes']:
                print("      Outcome:", outcome['name'], "Odds:", outcome['price'])
    print()
print("=" * 50)
