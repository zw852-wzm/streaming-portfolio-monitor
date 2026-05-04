from src.online_stats import initialize_state
from src.online_stats import compute_portfolio_return
from src.online_stats import update_state

def test_update_state_initializes_missing_optional_fields():
    state = initialize_state()

    del state["tail_event_count"]
    del state["recent_returns"]
    del state["rolling_window_size"]

    updated = update_state(state, 0.01)

    assert updated["tail_event_count"] == 0
    assert updated["recent_returns"] == [0.01]
    assert updated["rolling_window_size"] == 20

def test_update_state_trims_rolling_window():
    state = initialize_state()
    state["rolling_window_size"] = 2

    state = update_state(state, 0.01)
    state = update_state(state, 0.02)
    state = update_state(state, 0.03)

    assert state["recent_returns"] == [0.02, 0.03]

def test_update_state_computes_rolling_volatility_for_multiple_returns():
    state = initialize_state()
    state["rolling_window_size"] = 3

    state = update_state(state, 0.01)
    state = update_state(state, 0.03)

    assert state["rolling_volatility"] > 0


def test_compute_portfolio_return_ignores_unweighted_ticker():
    asset_returns = {
        "AAPL": 0.10,
        "MSFT": 0.20,
    }

    weights = {
        "AAPL": 0.50,
    }

    result = compute_portfolio_return(asset_returns, weights)

    assert result == 0.05

def test_compute_portfolio_return():
    asset_returns = {
        "AAPL": 0.10,
        "MSFT": 0.00
    }

    weights = {
        "AAPL": 0.50,
        "MSFT": 0.50
    }

    result = compute_portfolio_return(asset_returns, weights)

    assert result == 0.05


def test_update_state_one_return():
    state = initialize_state()

    state = update_state(state, 0.10)

    assert state["n"] == 1
    assert round(state["portfolio_value"], 4) == 1.1000
    assert round(state["running_mean"], 4) == 0.1000
    assert state["current_drawdown"] == 0.0
    assert state["max_drawdown"] == 0.0


def test_drawdown_after_loss():
    state = initialize_state()

    state = update_state(state, 0.10)
    state = update_state(state, -0.10)

    assert state["portfolio_value"] < state["running_peak"]
    assert state["current_drawdown"] < 0
    assert state["max_drawdown"] < 0


def test_tail_event_count():
    state = initialize_state()

    state = update_state(state, -0.03)

    assert state["tail_event_count"] == 1
