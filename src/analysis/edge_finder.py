from src.collectors.odds_collector import get_odds_data
from src.collectors.mlb_stats_collector import (
    calculate_team_trends,
    get_recent_games,
    calculate_streak,
)
from src.database.save_edge_reports import save_edge_report


def is_better_odds(new_odds, current_odds):
    # For positive odds, higher is better: +130 is better than +110
    if new_odds > 0 and current_odds > 0:
        return new_odds > current_odds

    # For negative odds, closer to zero is better: -120 is better than -150
    if new_odds < 0 and current_odds < 0:
        return new_odds > current_odds

    # Positive odds are generally better than negative odds for payout
    return new_odds > current_odds


def find_edges():
    odds_data = get_odds_data("baseball_mlb")
    recent_games = get_recent_games()
    trends = calculate_team_trends(recent_games)

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

            edge_score = trend_score + (odds / 100)

            streak = calculate_streak(stats["results"])

            if edge_score >= 2:
                signal = "Potential Value Bet"
            elif edge_score <= -2:
                signal = "Avoid / Cold Team"
            else:
                signal = "Neutral"

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
                "signal": signal
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
