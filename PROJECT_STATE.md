# Sports Betting Analytics Engine — Project State

## Project Goal

Build a sports betting analytics engine that collects live sportsbook odds, team performance data, pitcher data, and historical results, then generates custom betting recommendations based on a homemade odds/edge model.

The long-term goal is to create a system that:
- collects and stores large amounts of sports data
- compares sportsbook odds across books
- estimates fair odds using custom factors
- tracks line movement
- grades predictions after games finish
- tracks profitability over time
- posts recommendations through Discord

## Current Sport Focus

Current active sport:

```text
MLB

The project is currently focused on MLB because:
MLB is in season
daily games provide lots of data
odds move frequently
starting pitchers create meaningful edge opportunities
NFL support is planned later.
Current Working Features
The system currently can:
Pull MLB moneyline odds from The Odds API
Pull odds from multiple sportsbooks separately
Compare DraftKings, FanDuel, BetMGM, and Caesars when available
Merge sportsbook odds into event-level reports
Pull recent MLB game results from the MLB Stats API
Calculate team trends:
recent record
runs scored
runs allowed
run differential
current streak
Pull probable starting pitchers
Pull pitcher season stats:
ERA
WHIP
strikeouts
wins
losses
Calculate a rough pitcher score
Calculate trend score
Calculate edge score
Classify bets as:
OFFICIAL BET
Lean
Neutral
Avoid / Cold Team
Save edge reports to SQLite
View saved edge reports
Grade predictions after games complete
Simulate profit/loss
Run a Discord bot
Use !ping
Use !bets to return betting recommendations
Current Known Issues / Notes
Live games can produce extreme odds because live moneylines move during the game.
Some teams can play multiple games across adjacent days, so event grouping must include commence_time.
Odds should not be grouped only by team names.
The project currently needs stronger database structure for long-term analytics.
Current edge score is a rough prototype, not a mathematically validated betting model.
Need to move toward model-estimated win probability and fair odds.
Current Important Commands
Run odds collector:
python -m src.collectors.odds_collector

Run MLB stats collector:
python -m src.collectors.mlb_stats_collector

Run pitcher collector:
python -m src.collectors.mlb_pitcher_collector

Run edge finder:
python -m src.analysis.edge_finder

Run prediction grader:
python -m src.analysis.grade_predictions

Run Discord bot:
python -m src.discordbot.bot

Current File Structure
src/
  analysis/
    betting_objects.py
    edge_finder.py
    edge_model.py
    grade_predictions.py
    implied_probability.py
    line_movement.py

  collectors/
    mlb_pitcher_collector.py
    mlb_stats_collector.py
    odds_collector.py

  database/
    db.py
    save_edge_reports.py
    view_edge_reports.py

  discordbot/
    bot.py

Current Data Sources
The Odds API
Used for:
sportsbook odds
moneyline odds
bookmaker comparison
event commence times
MLB Stats API
Used for:
schedules
recent results
final scores
probable pitchers
pitcher stats
Current Model Inputs
Current edge model uses:
team recent record
team run differential
current streak
best available sportsbook odds
line difference between sportsbooks
pitcher score
recent momentum bonus
Current Model Direction
The model should evolve from:
edge score

toward:
estimated win probability
fair odds
sportsbook implied probability
model edge percentage

Example desired future output:
Team: Phillies
Model Win Probability: 61%
Model Fair Odds: -156
Best Sportsbook Odds: +110
Estimated Edge: +18.4%
Signal: OFFICIAL BET

Next Major Architecture Goal
Build a better database/data warehouse structure.
Future tables should include:
games
teams
sportsbooks
odds_snapshots
team_trends
pitchers
pitcher_stats
model_predictions
graded_results
weather
injuries
line_movement

Next Planned Work
Create a proper long-term database schema
Store games as unique events using event ID and commence time
Store odds snapshots separately from edge reports
Store model predictions separately from raw data
Add model-estimated win probability
Add fair odds conversion
Add implied probability comparison
Track closing line value
Improve prediction grading by signal type
Add better MLB factors:
home/away splits
bullpen fatigue
weather
park factor
lineup changes
handedness splits
Improve Discord commands later
Add README and portfolio documentation

Save it with:

```text
Ctrl + S

Then run:
git status
git add .
git commit -m "Add project state handoff document"
git push

That gives us a stable “resume point” for this entire project.

