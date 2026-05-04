# Streaming Portfolio Monitoring System

## Project Overview

This project implements a lightweight **streaming portfolio monitoring system** using daily financial data from Yahoo Finance.

Instead of storing and recomputing over the full historical dataset every time the program runs, the system treats financial data as a stream. Each run processes a new market observation, updates portfolio-level statistics incrementally, and saves the updated state for future runs.

The project demonstrates core data stream processing ideas, including online statistics, reservoir sampling, rolling-window metrics, duplicate-date protection, and persistent state management.

This is **not** a stock price prediction model or an automated trading strategy. The goal is to build a reproducible, memory-efficient monitoring pipeline for portfolio risk metrics.

---

## Dataset

The project uses daily market data from Yahoo Finance through the `yfinance` Python package.

The pipeline fetches the most recent **5 trading days** of data in order to compute the latest daily asset returns.

Current assets used in the portfolio:

```text
AAPL
MSFT
GLD
GOVT
BTC-USD
```

Each asset is assigned an equal portfolio weight:

```text
AAPL:    20%
MSFT:    20%
GLD:     20%
GOVT:    20%
BTC-USD: 20%
```

Because the data is fetched live from Yahoo Finance, output values may vary depending on the date and time the project is run.

---

## Core Pipeline

The system follows this pipeline:

```text
Fetch latest Yahoo Finance prices
        ↓
Compute latest asset returns
        ↓
Build one daily streaming record
        ↓
Load previous portfolio state from JSON
        ↓
Check whether the date has already been processed
        ↓
Compute weighted portfolio return
        ↓
Update online statistics and risk metrics
        ↓
Update reservoir sample
        ↓
Save updated state
        ↓
Print daily portfolio summary
```

In plain language:

```text
Get market data → calculate returns → update portfolio metrics → save state → print report
```

---

## Key Features

### Data Pipeline

- Fetches latest asset prices from Yahoo Finance
- Uses the most recent 5 trading days to compute latest daily returns
- Converts asset prices into daily returns
- Builds one streaming record per run
- Uses real financial market data

### Streaming Algorithms

- Online mean
- Online variance
- Constant-memory running statistics
- Reservoir sampling with fixed sample size
- Rolling-window tracking for recent returns

### Financial Metrics

The system tracks:

- Portfolio return
- Cumulative portfolio value
- Running volatility using all processed observations
- Rolling volatility using recent observations
- Current drawdown
- Maximum drawdown
- Tail risk event count
- Reservoir sample of past observations

### System Design

- Modular Python code structure
- Persistent state saved in JSON
- Automatic state directory creation
- Duplicate-date protection to avoid double counting
- Unit tests for core functionality
- Coverage reporting with `pytest-cov`

---

## Project Structure

```text
streaming-portfolio-monitor/
├── README.md
├── requirements.txt
├── setup.py
├── main.py
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── fetch_latest.py
│   ├── online_stats.py
│   ├── reporting.py
│   ├── sampling.py
│   └── state_manager.py
├── tests/
│   ├── test_fetch_latest.py
│   ├── test_online_stats.py
│   ├── test_reporting.py
│   ├── test_sampling.py
│   └── test_state_manager.py
└── data/
    └── state.json
```

Note: the `data/` directory and `data/state.json` are created during runtime if needed. The state file is not required before the first run.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/zw852-wzm/streaming-portfolio-monitor.git
cd streaming-portfolio-monitor
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install the project in editable mode:

```bash
pip install -e .
```

---

## How to Run

Run the main streaming portfolio monitor:

```bash
python3 main.py
```

Each run will:

1. Fetch the latest market data from Yahoo Finance
2. Generate one streaming record
3. Load the existing saved state
4. Check whether the current date was already processed
5. Compute the weighted portfolio return
6. Update portfolio statistics and risk metrics
7. Update the reservoir sample
8. Save the updated state
9. Print a daily portfolio summary

---

## Example Output

```text
================ Daily Portfolio Summary ================
Date: 2026-04-26
Portfolio Return: 0.20%
Portfolio Value: 1.001971

Risk Metrics:
Running Volatility: 0.00%
Rolling Volatility: 0.00%
Current Drawdown: 0.00%
Max Drawdown: 0.00%

Streaming Metrics:
Observations Processed: 1
Tail Events Count: 0
Reservoir Sample Size: 1
=========================================================
```

---

## State Persistence

The system saves its running state to:

```text
data/state.json
```

This state file allows the program to continue from previous runs instead of starting over every time.

The saved state includes information such as:

- Number of observations processed
- Running mean
- Running variance
- Portfolio value
- Drawdown metrics
- Rolling return window
- Reservoir sample
- Processed dates

To reset the system, delete the state file:

```bash
rm -f data/state.json
```

Then run the program again:

```bash
python3 main.py
```

---

## Duplicate Date Protection

The system keeps track of previously processed dates.

If the same date is processed again, the program will skip the update to avoid double counting.

Example:

```text
Date 2026-04-26 has already been processed. No update performed.
```

This makes the streaming update safer when the program is run multiple times on the same day.

---

## Testing

Run all unit tests:

```bash
python -m pytest -q
```

Run tests with coverage:

```bash
python -m pytest --cov=src tests/ --cov-report=term-missing
```

Current local test result:

```text
21 passed
Total coverage: 100%
```

The tests cover:

- Yahoo Finance data processing helpers
- Portfolio return calculation
- Online statistics updates
- Reservoir sampling
- State saving and loading
- Daily summary reporting

---

## Main Modules

### `src/fetch_latest.py`

Handles market data ingestion.

Main responsibilities:

- Fetch latest prices using `yfinance`
- Compute latest asset returns
- Build a daily streaming record

### `src/online_stats.py`

Contains the core portfolio monitoring logic.

Main responsibilities:

- Initialize portfolio state
- Compute weighted portfolio return
- Update online mean
- Update online variance
- Update portfolio value
- Track running volatility
- Track rolling volatility
- Track current drawdown
- Track maximum drawdown
- Track tail risk events

### `src/sampling.py`

Implements reservoir sampling.

Main responsibilities:

- Maintain a fixed-size random sample of past streaming records
- Avoid storing the full stream history
- Support memory-efficient stream sampling

### `src/state_manager.py`

Handles state persistence.

Main responsibilities:

- Load portfolio state from JSON
- Save portfolio state to JSON
- Create the state directory automatically if needed

### `src/reporting.py`

Formats and prints the daily portfolio report.

Main responsibilities:

- Format decimal returns as percentages
- Print portfolio return
- Print portfolio value
- Print risk metrics
- Print streaming metrics

---

## Key Concepts

### Streaming Data

A data stream is a sequence of observations that arrive over time. In this project, each new daily market observation is treated as one item in the stream.

### Online Statistics

Online algorithms update statistics incrementally without storing all past data.

For example, instead of keeping every past return to recompute the mean, the system updates the running mean using only the previous state and the new observation.

### Reservoir Sampling

Reservoir sampling keeps a fixed-size random sample from a stream.

This is useful when the stream is too large to store fully, but we still want a representative sample of past observations.

### Rolling Volatility

Rolling volatility measures recent risk using a limited window of recent returns.

This is different from running volatility, which uses all processed observations.

### Drawdown

Drawdown measures how much the portfolio value has fallen from its historical peak.

Maximum drawdown tracks the worst peak-to-trough loss observed so far.

### Tail Risk

Tail risk focuses on extreme negative returns. It helps monitor unusually bad portfolio outcomes.

---

## Reproducibility Notes

This project is designed to be reproducible in structure, testing, and execution commands.

However, the main program uses live Yahoo Finance data, so the exact portfolio return and risk metrics may change depending on when the project is run.

For reproducible validation, use the unit tests:

```bash
python -m pytest --cov=src tests/ --cov-report=term-missing
```

The tests use controlled inputs and do not depend on unpredictable live market output.

---

## Future Improvements

Possible extensions include:

- Add an offline demo with fixed sample returns
- Add visualization for portfolio value and drawdown
- Add Value-at-Risk and Conditional Value-at-Risk
- Add support for custom tickers and custom weights
- Add a command-line interface
- Add a dashboard for monitoring metrics
- Add intraday data support
- Add structured logging
- Add parallel processing for larger portfolios
- Deploy the monitor as a lightweight real-time service

---

## Authors

- Zimo Wu
- Weijia Jin

---

## Acknowledgment

This project was developed for ORIE 5270 Big Data Technologies as a final project focused on data stream processing, reproducible software design, and unit-tested computational pipelines.
