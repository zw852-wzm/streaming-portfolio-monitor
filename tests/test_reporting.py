from src.reporting import format_percent


def test_format_percent_positive():
    assert format_percent(0.0123) == "1.23%"


def test_format_percent_negative():
    assert format_percent(-0.0456) == "-4.56%"


def test_format_percent_zero():
    assert format_percent(0.0) == "0.00%"