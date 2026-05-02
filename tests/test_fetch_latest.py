import pandas as pd

from src.fetch_latest import compute_latest_returns
from src.fetch_latest import build_stream_record


def test_compute_latest_returns():
    prices = pd.DataFrame({
        "AAPL": [100.0, 110.0],
        "MSFT": [200.0, 220.0],
    })

    latest_returns = compute_latest_returns(prices)

    assert round(latest_returns["AAPL"], 4) == 0.1000
    assert round(latest_returns["MSFT"], 4) == 0.1000


def test_build_stream_record():
    latest_returns = pd.Series(
        data={"AAPL": 0.01, "MSFT": -0.02},
        name=pd.Timestamp("2026-04-26")
    )

    record = build_stream_record(latest_returns)

    assert record["date"] == "2026-04-26"
    assert record["returns"]["AAPL"] == 0.01
    assert record["returns"]["MSFT"] == -0.02