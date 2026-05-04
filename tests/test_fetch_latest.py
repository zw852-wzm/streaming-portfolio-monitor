import pandas as pd
from unittest.mock import patch

from src.fetch_latest import fetch_latest_prices
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

def test_fetch_latest_prices_returns_close_prices():
    index = pd.to_datetime(["2026-04-24", "2026-04-25"])

    fake_data = pd.DataFrame(
        {
            ("Close", "AAPL"): [100.0, 101.0],
            ("Close", "MSFT"): [200.0, 202.0],
        },
        index=index,
    )

    fake_data.columns = pd.MultiIndex.from_tuples(fake_data.columns)

    with patch("src.fetch_latest.yf.download", return_value=fake_data) as mock_download:
        prices = fetch_latest_prices(["AAPL", "MSFT"])

    mock_download.assert_called_once_with(
        ["AAPL", "MSFT"],
        period="5d",
        interval="1d",
        auto_adjust=True,
        progress=False,
    )

    expected = fake_data["Close"]
    pd.testing.assert_frame_equal(prices, expected)
