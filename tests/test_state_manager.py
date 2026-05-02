from src.state_manager import save_state, load_state

def test_save_and_load(tmp_path):
    filepath = tmp_path / "state.json"

    state = {"n": 1}
    save_state(state, filepath)

    loaded = load_state(filepath)

    assert loaded["n"] == 1