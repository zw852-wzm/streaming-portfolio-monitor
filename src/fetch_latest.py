import yfinance as yf
import pandas as pd


def fetch_latest_prices(tickers):
    """
    Fetch the most recent daily closing prices from Yahoo Finance.

    Parameters
    ----------
    tickers : list[str]
        A list of ticker symbols, such as ["AAPL", "MSFT", "GLD"].

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing recent adjusted close prices.
    """

    data = yf.download(
        tickers,
        period="5d",
        interval="1d",
        auto_adjust=True,
        progress=False
    )

    prices = data["Close"]

    return prices

def compute_latest_returns(prices):
    """
    Convert price data into the most recent daily returns.

    Parameters
    ----------
    prices : pandas.DataFrame
        DataFrame of adjusted close prices.

    Returns
    -------
    pandas.Series
        The most recent daily returns for each asset.
    """

    returns = prices.pct_change(fill_method=None).dropna(how="all")

    latest_returns = returns.iloc[-1]

    return latest_returns

def build_stream_record(latest_returns):
    """
    Build a streaming record from the latest returns.

    Parameters
    ----------
    latest_returns : pandas.Series

    Returns
    -------
    dict
        A streaming event containing date and asset returns.
    """

    record = {
        "date": latest_returns.name.strftime("%Y-%m-%d"),
        "returns": latest_returns.dropna().to_dict()
    }

    return record