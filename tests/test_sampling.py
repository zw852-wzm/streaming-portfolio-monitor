from src.sampling import update_reservoir_sample


def test_reservoir_sample_grows_until_k():
    sample = []
    k = 5

    for i in range(3):
        record = {"date": f"day_{i}", "portfolio_return": i}
        sample = update_reservoir_sample(sample, record, n_seen=i + 1, k=k)

    assert len(sample) == 3


def test_reservoir_sample_never_exceeds_k():
    sample = []
    k = 5

    for i in range(100):
        record = {"date": f"day_{i}", "portfolio_return": i}
        sample = update_reservoir_sample(sample, record, n_seen=i + 1, k=k)

    assert len(sample) == k


def test_reservoir_sample_records_have_required_fields():
    sample = []
    k = 5

    record = {
        "date": "2026-04-26",
        "portfolio_return": 0.01,
        "asset_returns": {"AAPL": 0.01}
    }

    sample = update_reservoir_sample(sample, record, n_seen=1, k=k)

    assert "date" in sample[0]
    assert "portfolio_return" in sample[0]
    assert "asset_returns" in sample[0]