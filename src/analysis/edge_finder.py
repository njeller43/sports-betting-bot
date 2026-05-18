from src.collectors.odds_collector import get_all_bookmaker_odds
from src.collectors.mlb_stats_collector import (
    calculate_team_trends,
    get_recent_games,
    calculate_streak,
    calculate_recent_offense
)
from src.analysis.edge_model import (
    is_better_odds,
    calculate_recent_bonus,
    calculate_edge_score,
    classify_signal
)
from src.database.save_edge_reports import save_edge_report
from src.collectors.mlb_pitcher_collector import (
    get_today_pitchers,
    get_pitcher_stats,
    calculate_pitcher_score,
)
from datetime import datetime, timezone
from src.database.warehouse import save_model_prediction
from src.analysis.edge_model import estimate_win_probability
from src.analysis.probability_model import (
    calculate_market_edge,
    probability_to_american_odds,
)
from src.collectors.mlb_bullpen_collector import (
    get_recent_games as get_recent_bullpen_games,
    calculate_bullpen_fatigue_score,
    calculate_bullpen_usage
)
from src.analysis.park_factors import calculate_park_factor_bonus

from src.collectors.weather_collector import (
    get_weather,
    calculate_weather_bonus
)

from datetime import datetime, timedelta, timezone


def format_eastern_time(utc_time_string):

    utc_time = datetime.fromisoformat(
        utc_time_string.replace("Z", "+00:00")
    )

    eastern_time = utc_time - timedelta(hours=4)

    return eastern_time.strftime("%I:%M %p ET")

def build_pitcher_lookup(pitcher_data):

    pitcher_lookup = {}

    for date in pitcher_data.get("dates", []):
        for game in date.get("games", []):

            away_team = game["teams"]["away"]["team"]["name"]
            home_team = game["teams"]["home"]["team"]["name"]

            away_pitcher = (
                game["teams"]["away"]
                .get("probablePitcher", {})
            )

            home_pitcher = (
                game["teams"]["home"]
                .get("probablePitcher", {})
            )

            pitcher_lookup[away_team] = away_pitcher
            pitcher_lookup[home_team] = home_pitcher

    return pitcher_lookup

def find_edges():
    odds_data = get_all_bookmaker_odds("baseball_mlb")
    recent_games = get_recent_games()
    trends = calculate_team_trends(recent_games)
    bullpen_games = get_recent_bullpen_games()
    bullpen_usage = calculate_bullpen_usage(bullpen_games)
    pitcher_data = get_today_pitchers()
    pitcher_lookup = build_pitcher_lookup(pitcher_data)

    edge_reports = []

    for event in odds_data:
        commence_time = event["commence_time"]

        game_date = datetime.fromisoformat(
            commence_time.replace("Z", "+00:00")
        ).date()

        today = datetime.now(timezone.utc).date()

        if game_date != today:
            continue

        home_team = event["home_team"]
        away_team = event["away_team"]

        print()
        print("=" * 60)
        print(f"{away_team} vs {home_team}")
        print(f"Game Time: {format_eastern_time(commence_time)}")
        print(f"Event ID: {event['id']}")
        print("=" * 60)

        best_lines = {}
        all_lines = {}

        for bookmaker in event["bookmakers"]:
            sportsbook = bookmaker["title"]

            for market in bookmaker["markets"]:
                if market["key"] != "h2h":
                    continue
                for outcome in market["outcomes"]:
                    team = outcome["name"]
                    odds = outcome["price"]

                    if team not in all_lines:
                        all_lines[team] = []

                    all_lines[team].append({
                        "odds": odds,
                        "sportsbook": sportsbook,
                    })

                    if team not in best_lines:
                        best_lines[team] = {
                            "odds": odds,
                            "sportsbook": sportsbook,
                        }
                    elif is_better_odds(odds, best_lines[team]["odds"]):
                        best_lines[team] = {
                            "odds": odds,
                            "sportsbook": sportsbook,
                        }

        for team, line_data in best_lines.items():
            odds = line_data["odds"]
            sportsbook = line_data["sportsbook"]
            team_lines = all_lines[team]
            all_odds = [line["odds"] for line in team_lines]

            highest_odds = max(all_odds)
            lowest_odds = min(all_odds)

            line_difference = highest_odds - lowest_odds

            if team not in trends:
                continue

            stats = trends[team]

            bullpen_stats = bullpen_usage.get(team, {"bullpen_appearances": 0})
            bullpen_fatigue_score = calculate_bullpen_fatigue_score(bullpen_stats)

            run_diff = stats["runs_scored"] - stats["runs_allowed"]
            recent_offense = calculate_recent_offense(stats["recent_runs"])
            offense_bonus = ( recent_offense -4.5) * 0.8

            park_factor_bonus = calculate_park_factor_bonus(
                home_team)
            
            weather = get_weather(home_team)
            weather_bonus = calculate_weather_bonus(weather)

            trend_score = (
                (stats["wins"] - stats["losses"])
                + (run_diff / 10)
            )

            if team == home_team:
                split_wins = stats["home_wins"]
                split_losses = stats["home_losses"]
            else:
                split_wins = stats["away_wins"]
                split_losses = stats["away_losses"]

            home_away_bonus = (split_wins - split_losses) * 0.5

            pitcher_info = pitcher_lookup.get(team, {})

            pitcher_name = pitcher_info.get("fullName", "TBD")
            pitcher_id = pitcher_info.get("id")

            pitcher_stats = get_pitcher_stats(pitcher_id)
            pitcher_score = calculate_pitcher_score(pitcher_stats)

            recent_bonus = calculate_recent_bonus(stats["results"])

            edge_score = calculate_edge_score(
                trend_score + 
                home_away_bonus + 
                offense_bonus + 
                park_factor_bonus + 
                weather_bonus,
                odds,
                pitcher_score + bullpen_fatigue_score,
                recent_bonus,
            )

            model_win_probability = estimate_win_probability(edge_score)

            fair_odds = probability_to_american_odds(
                model_win_probability
            )
            market_edge = calculate_market_edge(
                model_win_probability,
                odds
            )

            streak = calculate_streak(stats["results"])
            
            signal = classify_signal(edge_score)

            edge_reports.append({
                "event": f"{away_team} vs {home_team}",
                "team": team,
                "odds": odds,
                "sportsbook": sportsbook,
                "team_lines": team_lines,
                "line_difference": line_difference,
                "record" : f"{stats['wins']}-{stats['losses']}",
                "run_diff": run_diff,
                "trend_score": trend_score,
                "edge_score": edge_score,
                "streak": streak,
                "signal": signal,
                "pitcher_name": pitcher_name,
                "pitcher_score": pitcher_score,
                "external_event_id": event["id"],
                "sport": "baseball_mlb",
                "home_team": home_team,
                "away_team": away_team,
                "commence_time": event["commence_time"],
                "model_win_probability": model_win_probability,
                "fair_odds": fair_odds,
                "market_edge": market_edge,
                "home_away_bonus": home_away_bonus,
                "bullpen_fatigue_score": bullpen_fatigue_score,
                "recent_offense": recent_offense,
                "offense_bonus": offense_bonus,
                "park_factor_bonus": park_factor_bonus,
                "weather": weather,
                "weather_bonus": weather_bonus,
            })

            
    edge_reports.sort(
        key=lambda report: report["edge_score"],
        reverse=True
    )

    print()
    print("=" * 60)
    print("TOP EDGE REPORT")
    print("=" * 60)

    for report in edge_reports:
        save_edge_report(report)
        save_model_prediction(
            external_event_id=report["external_event_id"],
            sport=report["sport"],
            home_team=report["home_team"],
            away_team=report["away_team"],
            commence_time=report["commence_time"],
            team=report["team"],
            sportsbook=report["sportsbook"],
            odds=report["odds"],
            trend_score=report["trend_score"],
            pitcher_score=report["pitcher_score"],
            edge_score=report["edge_score"],
            signal=report["signal"],
            model_win_probability=report["model_win_probability"]
        )
        print()
        print(report["event"])

        print(f"Team: {report['team']}")
        print(
            f"Best Odds: "
            f"{report['odds']} "
            f"({report['sportsbook']})"
        )

        print("Sportsbook Lines:")

        for line in report["team_lines"]:
            print(
                f"  {line['sportsbook']}: "
                f"{line['odds']}"
            )

        print(
            f"Line Difference: "
            f"{report['line_difference']:+}"
        )

        print(f"Record: {report['record']}")
        print(f"Run Differential: {report['run_diff']:+}")

        print(
            f"Trend Score: "
            f"{report['trend_score']:+.1f}"
        )

        print(f"Pitcher: {report['pitcher_name']}")
        print(f"Pitcher Score: {report['pitcher_score']:+.2f}"
        )

        print(
            f"Edge Score: "
            f"{report['edge_score']:+.2f}"
        )

        print(f"Current Streak: {report['streak']}")

        if report["edge_score"] >= 2:
            print("Signal: Potential Value Bet")

        elif report["edge_score"] <= -2:
            print("Signal: Avoid / Cold Team")

        else:
            print("Signal: Neutral")
    
    print(
        f"Model Win Probability: {report['model_win_probability']}%"
    )
    print(
        f"Fair Odds: {report['fair_odds']}"
    )
    print(
        f"Market Edge: {report['market_edge']:+.2f}%"
    )

    print(
        f"Home/Away Bonus: {report['home_away_bonus']:+.2f}"
    )
    print(
        f"Bullpen Fatigue Score: {report['bullpen_fatigue_score']:+.1f}"
    )
    print(
        f"Recent Offensive Rating: {report['recent_offense']:.2f}"
    )
    print(
        f"Offense Bonus: {report['offense_bonus']:+.2f}"
    )
    print(
        f"Park Factor Bonus: {report['park_factor_bonus']:+.2f}"
    )

    print(
        f"Weather: "
        f"{report['weather']['temperature']}°F, "
        f"Wind {report['weather']['wind_speed']} mph"
    )

    print(
        f"Weather Bonus: {report['weather_bonus']:+.2f}"
    )

    return edge_reports
if __name__ == "__main__":
    find_edges()
