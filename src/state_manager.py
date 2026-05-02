import json
import os

from src.online_stats import initialize_state


def load_state(filepath="data/state.json"):
    """
    Load portfolio state from a JSON file.
    If the file does not exist, initialize a new state.

    Parameters
    ----------
    filepath : str
        Path to the state JSON file.

    Returns
    -------
    dict
        Portfolio monitoring state.
    """

    if not os.path.exists(filepath):
        return initialize_state()

    with open(filepath, "r") as f:
        state = json.load(f)

    return state


def save_state(state, filepath="data/state.json"):
    """
    Save portfolio state to a JSON file.

    Parameters
    ----------
    state : dict
        Portfolio monitoring state.

    filepath : str
        Path to the state JSON file.
    """

    with open(filepath, "w") as f:
        json.dump(state, f, indent=4)