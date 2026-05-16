from src.collectors.odds_collector import get_odds_data
from src.collectors.mlb_stats_collector import (
    calculate_team_trends,
    get_recent_games,
    calculate_streak,
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
    odds_data = get_odds_data("baseball_mlb")
    recent_games = get_recent_games()
    trends = calculate_team_trends(recent_games)
    pitcher_data = get_today_pitchers()
    pitcher_lookup = build_pitcher_lookup(pitcher_data)

    edge_reports = []

    for event in odds_data:
        home_team = event["home_team"]
        away_team = event["away_team"]

        print()
        print("=" * 60)
        print(f"{away_team} vs {home_team}")
        print("=" * 60)

        best_lines = {}
        all_lines = {}

        for bookmaker in event["bookmakers"]:
            sportsbook = bookmaker["title"]

            for market in bookmaker["markets"]:
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

            run_diff = stats["runs_scored"] - stats["runs_allowed"]

            trend_score = (
                (stats["wins"] - stats["losses"])
                + (run_diff / 10)
            )

            pitcher_info = pitcher_lookup.get(team, {})

            pitcher_name = pitcher_info.get("fullName", "TBD")
            pitcher_id = pitcher_info.get("id")

            pitcher_stats = get_pitcher_stats(pitcher_id)
            pitcher_score = calculate_pitcher_score(pitcher_stats)

            recent_bonus = calculate_recent_bonus(stats["results"])

            edge_score = calculate_edge_score(
                trend_score,
                odds,
                pitcher_score,
                recent_bonus,
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


if __name__ == "__main__":
    find_edges()
