def initialize_state():
    """
    Initialize the portfolio monitoring state.

    Returns
    -------
    dict
        Initial state for online portfolio metrics.
    """

    return {
        "n": 0,
        "portfolio_value": 1.0,
        "running_mean": 0.0,
        "running_M2": 0.0,
        "running_variance": 0.0,
        "running_volatility": 0.0,
        "running_peak": 1.0,
        "current_drawdown": 0.0,
        "max_drawdown": 0.0,
        "tail_event_count": 0,
        "processed_dates": [],
        "reservoir_sample": [],
        "rolling_window_size": 20,
        "recent_returns": [],
        "rolling_mean": 0.0,
        "rolling_volatility": 0.0
    }


def compute_portfolio_return(asset_returns, weights):
    """
    Compute portfolio return from asset returns and portfolio weights.

    Parameters
    ----------
    asset_returns : dict
        Asset returns from one streaming record.

    weights : dict
        Portfolio weights for each asset.

    Returns
    -------
    float
        Portfolio daily return.
    """

    portfolio_return = 0.0

    for ticker, r in asset_returns.items():
        if ticker in weights:
            portfolio_return += weights[ticker] * r

    return portfolio_return


def update_state(state, portfolio_return):
    """
    Update portfolio state using one new portfolio return.

    Parameters
    ----------
    state : dict
        Current portfolio state.

    portfolio_return : float
        New portfolio return from the latest stream record.

    Returns
    -------
    dict
        Updated portfolio state.
    """

    TAIL_THRESHOLD = -0.02

    if "tail_event_count" not in state:
        state["tail_event_count"] = 0

    state["n"] += 1
    n = state["n"]

    state["portfolio_value"] *= (1 + portfolio_return)

    old_mean = state["running_mean"]
    new_mean = old_mean + (portfolio_return - old_mean) / n

    state["running_mean"] = new_mean
    state["running_M2"] += (portfolio_return - old_mean) * (portfolio_return - new_mean)

    if n > 1:
        state["running_variance"] = state["running_M2"] / (n - 1)
        state["running_volatility"] = state["running_variance"] ** 0.5

    state["running_peak"] = max(
        state["running_peak"],
        state["portfolio_value"]
    )

    state["current_drawdown"] = (
        state["portfolio_value"] / state["running_peak"] - 1
    )

    state["max_drawdown"] = min(
        state["max_drawdown"],
        state["current_drawdown"]
    )

    if portfolio_return < TAIL_THRESHOLD:
        state["tail_event_count"] += 1

    if "recent_returns" not in state:
        state["recent_returns"] = []

    if "rolling_window_size" not in state:
        state["rolling_window_size"] = 20

    state["recent_returns"].append(portfolio_return)

    if len(state["recent_returns"]) > state["rolling_window_size"]:
        state["recent_returns"].pop(0)

    window = state["recent_returns"]

    if len(window) > 0:
        state["rolling_mean"] = sum(window) / len(window)

    if len(window) > 1:
        squared_diffs = [
            (r - state["rolling_mean"]) ** 2
            for r in window
        ]

        state["rolling_volatility"] = (
            sum(squared_diffs) / (len(window) - 1)
        ) ** 0.5
    else:
        state["rolling_volatility"] = 0.0

    return state