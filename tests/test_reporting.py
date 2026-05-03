from src.reporting import format_percent, print_daily_summary


def test_format_percent_positive():
    assert format_percent(0.0123) == "1.23%"


def test_format_percent_negative():
    assert format_percent(-0.0456) == "-4.56%"


def test_format_percent_zero():
    assert format_percent(0.0) == "0.00%"

def test_print_daily_summary_outputs_expected_fields(capsys):
    record = {
        "date": "2026-04-26",
        "returns": {
            "AAPL": 0.01,
            "MSFT": -0.005,
        },
    }

    portfolio_return = 0.002

    state = {
        "portfolio_value": 1.001971,
        "running_volatility": 0.03,
        "rolling_volatility": 0.02,
        "current_drawdown": 0.01,
        "max_drawdown": 0.05,
        "n": 5,
        "tail_event_count": 1,
        "reservoir_sample": [
            {"date": "2026-04-26", "portfolio_return": 0.002}
        ],
    }

    print_daily_summary(record, portfolio_return, state)

    captured = capsys.readouterr()
    output = captured.out

    assert "Daily Portfolio Summary" in output
    assert "Date: 2026-04-26" in output
    assert "Portfolio Return: 0.20%" in output
    assert "Portfolio Value: 1.001971" in output
    assert "Risk Metrics:" in output
    assert "Running Volatility: 3.00%" in output
    assert "Rolling Volatility: 2.00%" in output
    assert "Current Drawdown: 1.00%" in output
    assert "Max Drawdown: 5.00%" in output
    assert "Streaming Metrics:" in output
    assert "Observations Processed: 5" in output
    assert "Tail Events Count: 1" in output
    assert "Reservoir Sample Size: 1" in output
