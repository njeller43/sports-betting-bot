import os
import requests

from dotenv import load_dotenv
from src.analysis.implied_probability import american_odds_to_probability
from src.analysis.betting_objects import create_betting_object
from src.database.db import create_tables, create_collection_run, insert_betting_odds
from src.database.warehouse import save_odds_snapshot
load_dotenv()

API_KEY = os.getenv("ODDS_API_KEY")

BOOKMAKERS = ["draftkings", "fanduel", "betmgm", "caesars"]

def get_odds_data(sport="baseball_mlb", bookmaker="draftkings"):
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"

    params = {
    "apiKey": API_KEY,
    "regions": "us",
    "markets": "h2h",
    "bookmakers": bookmaker,
    "oddsFormat": "american"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Error fetching odds data:", response.status_code, response.text)
        return []

    data = response.json()
    return data           

def get_all_bookmaker_odds(sport="baseball_mlb"):
    events_by_matchup = {}

    for bookmaker in BOOKMAKERS:
        print(f"Fetching odds from {bookmaker}...")

        bookmaker_events = get_odds_data(
            sport=sport,
            bookmaker=bookmaker
        )

        for event in bookmaker_events:
            matchup_key = tuple(sorted([
                event["home_team"],
                event["away_team"]
            ]))

            if matchup_key not in events_by_matchup:
                events_by_matchup[matchup_key] = event
            else:
                events_by_matchup[matchup_key]["bookmakers"].extend(
                    event.get("bookmakers", [])
                )

    return list(events_by_matchup.values())

def display_odds(events, sport):
    betting_objects = []

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
                    save_odds_snapshot(
                        external_event_id=event['id'],
                        sport=sport,
                        home_team=event['home_team'],
                        away_team=event['away_team'],
                        commence_time=event['commence_time'],
                        sportsbook_name=bookmaker['title'],
                        team=outcome['name'],
                        market=market['key'],
                        odds=outcome['price'],
                        implied_probability=probability
                    )
                    betting_object = create_betting_object(
                        sport=sport,
                        event_name=f"{event['home_team']} vs {event['away_team']}",
                        sportsbook=bookmaker['title'],
                        team=outcome['name'],
                        odds=outcome['price'],
                        implied_probability=probability
                    )
                    betting_objects.append(betting_object)
                    print(betting_object)

    return betting_objects

if __name__ == "__main__":
    create_tables()

    run_id = create_collection_run()

    sport="baseball_mlb"
    odds_data = get_all_bookmaker_odds(sport=sport)
    all_bets = display_odds(odds_data, sport)

    insert_betting_odds(all_bets, run_id)

    print()
    print(f"Collection Run ID: {run_id}")
    print(f"Total Bets Collected: {len(all_bets)}")
    print("Betting odds saved into database successfully.")

