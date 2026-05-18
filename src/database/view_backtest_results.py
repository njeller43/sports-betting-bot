from src.database.schema import get_connection


def view_backtest_results():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) AS total_bets,
            SUM(gr.prediction_correct) AS wins,
            SUM(CASE WHEN gr.prediction_correct = 0 THEN 1 ELSE 0 END) AS losses,
            SUM(gr.profit_loss) AS total_units,
            AVG(gr.profit_loss) AS avg_units_per_bet
        FROM graded_results gr
    """)

    summary = cursor.fetchone()

    total_bets, wins, losses, total_units, avg_units = summary

    print()
    print("=" * 60)
    print("OVERALL BACKTEST SUMMARY")
    print("=" * 60)

    if not total_bets:
        print("No graded results yet.")
        conn.close()
        return

    win_rate = (wins / total_bets) * 100

    print(f"Total Bets: {total_bets}")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Win Rate: {win_rate:.2f}%")
    print(f"Total Units: {total_units:+.2f}")
    print(f"Average Units Per Bet: {avg_units:+.3f}")

    print()
    print("=" * 60)
    print("PERFORMANCE BY SIGNAL")
    print("=" * 60)

    cursor.execute("""
        SELECT
            mp.signal,
            COUNT(*) AS total_bets,
            SUM(gr.prediction_correct) AS wins,
            SUM(CASE WHEN gr.prediction_correct = 0 THEN 1 ELSE 0 END) AS losses,
            SUM(gr.profit_loss) AS total_units,
            AVG(gr.profit_loss) AS avg_units_per_bet
        FROM graded_results gr
        JOIN model_predictions mp
            ON gr.prediction_id = mp.id
        GROUP BY mp.signal
        ORDER BY total_units DESC
    """)

    rows = cursor.fetchall()

    for row in rows:
        signal, total, signal_wins, signal_losses, signal_units, signal_avg = row
        signal_win_rate = (signal_wins / total) * 100

        print()
        print(f"Signal: {signal}")
        print(f"Total Bets: {total}")
        print(f"Wins: {signal_wins}")
        print(f"Losses: {signal_losses}")
        print(f"Win Rate: {signal_win_rate:.2f}%")
        print(f"Total Units: {signal_units:+.2f}")
        print(f"Average Units Per Bet: {signal_avg:+.3f}")

    conn.close()


if __name__ == "__main__":
    view_backtest_results()