def format_percent(value):
    """
    Convert a decimal return into a percentage string.
    Example: 0.0123 -> 1.23%
    """

    return f"{value * 100:.2f}%"


def print_daily_summary(record, portfolio_return, state):
    """
    Print a clean daily portfolio monitoring summary.
    """

    print("\n================ Daily Portfolio Summary ================")

    print(f"Date: {record['date']}")
    print(f"Portfolio Return: {format_percent(portfolio_return)}")
    print(f"Portfolio Value: {state['portfolio_value']:.6f}")

    print("\nRisk Metrics:")
    print(f"Running Volatility: {format_percent(state['running_volatility'])}")
    print(f"Rolling Volatility: {format_percent(state['rolling_volatility'])}")
    print(f"Current Drawdown: {format_percent(state['current_drawdown'])}")
    print(f"Max Drawdown: {format_percent(state['max_drawdown'])}")

    print("\nStreaming Metrics:")
    print(f"Observations Processed: {state['n']}")
    print(f"Tail Events Count: {state['tail_event_count']}")
    print(f"Reservoir Sample Size: {len(state['reservoir_sample'])}")

    print("=========================================================\n")