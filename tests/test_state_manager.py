from src.state_manager import save_state, load_state
from src.online_stats import initialize_state

def test_load_state_missing_file_returns_initialized_state(tmp_path):
    filepath = tmp_path / "missing_state.json"

    state = load_state(filepath)

    expected = initialize_state()

    assert state["n"] == expected["n"]
    assert state["portfolio_value"] == expected["portfolio_value"]
    assert state["running_mean"] == expected["running_mean"]
    assert state["processed_dates"] == expected["processed_dates"]


def test_save_state_creates_directory(tmp_path):
    filepath = tmp_path / "nested" / "state.json"
    state = {"n": 3}

    save_state(state, filepath)

    assert filepath.exists()

    loaded = load_state(filepath)
    assert loaded["n"] == 3


def test_save_and_load(tmp_path):
    filepath = tmp_path / "state.json"

    state = {"n": 1}
    save_state(state, filepath)

    loaded = load_state(filepath)

    assert loaded["n"] == 1
