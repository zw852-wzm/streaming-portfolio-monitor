from src.fetch_latest import fetch_latest_prices
from src.fetch_latest import compute_latest_returns
from src.fetch_latest import build_stream_record

from src.online_stats import compute_portfolio_return
from src.online_stats import update_state

from src.state_manager import load_state
from src.state_manager import save_state
from src.sampling import update_reservoir_sample
from src.reporting import print_daily_summary

def main():
    tickers = ["AAPL", "MSFT", "GLD", "GOVT", "BTC-USD"]

    weights = {
        "AAPL": 0.20,
        "MSFT": 0.20,
        "GLD": 0.20,
        "GOVT": 0.20,
        "BTC-USD": 0.20
    }

    prices = fetch_latest_prices(tickers)
    latest_returns = compute_latest_returns(prices)
    record = build_stream_record(latest_returns)

    print("Streaming record:")
    print(record)

    state = load_state()

    if "processed_dates" not in state:
        state["processed_dates"] = []

    if record["date"] in state["processed_dates"]:
        print(f"\nDate {record['date']} has already been processed. No update performed.")
        return

    portfolio_return = compute_portfolio_return(
        record["returns"],
        weights
    )

    state = update_state(state, portfolio_return)

    if "reservoir_sample" not in state:
        state["reservoir_sample"] = []

    sample_record = {
        "date": record["date"],
        "portfolio_return": portfolio_return,
        "asset_returns": record["returns"]
    }

    state["reservoir_sample"] = update_reservoir_sample(
        state["reservoir_sample"],
        sample_record,
        state["n"],
        k=5
    )


    state["processed_dates"].append(record["date"])

    save_state(state)

    print_daily_summary(record, portfolio_return, state)


if __name__ == "__main__":
    main()