# Streaming Portfolio Monitoring System

## 1. Project Overview

This project implements a **streaming portfolio monitoring system** using real financial data from Yahoo Finance.

Instead of storing and recomputing statistics from full historical datasets, the system processes **one new market observation at a time** and updates portfolio metrics incrementally using **online algorithms**.

The goal is to simulate a real-world financial monitoring pipeline that is:

- Incremental (process data as it arrives)
- Memory-efficient (no need to store full history)
- Reproducible (persistent state)
- Modular and testable

---

## 2. Dataset

This project uses financial market data from **Yahoo Finance** via the `yfinance` API.

### Assets
- AAPL (Apple)
- MSFT (Microsoft)
- GLD (Gold ETF)
- GOVT (US Treasury ETF)
- BTC-USD (Bitcoin)

### Data Characteristics
- Frequency: Daily  
- Source: Yahoo Finance API  
- Window: Last 5 trading days (rolling fetch)

⚠️ Note: Results may vary depending on the execution date since data is live.

---

## 3. Key Features

### Streaming Data Pipeline
- Fetch latest asset prices
- Convert prices to returns
- Build a streaming record

### Online Algorithms
- Running mean
- Running variance & volatility
- Rolling window statistics
- Drawdown tracking

### Risk Metrics
- Portfolio return
- Portfolio value
- Running volatility
- Rolling volatility
- Drawdown
- Tail event count

### System Design
- Modular package structure
- Persistent state (JSON)
- Duplicate-date protection
- Unit tests

---

## 4. Project Structure

streaming_portfolio_monitor/
├── src/
├── tests/
├── data/
├── main.py
├── setup.py
├── requirements.txt
└── README.md

---

## 5. Installation

pip3 install -r requirements.txt  
pip3 install -e .

---

## 6. How to Run

python3 main.py

---

## 7. What Happens When You Run
Each execution performs the following steps:

1. Fetch market data  
2. Compute returns  
3. Build record  
4. Check duplicate  
5. Compute portfolio return  
6. Update state  
7. Update sample  
8. Save state  
9. Print summary  

---

## 8. Example Output

Date: 2026-04-26  
Portfolio Return: 0.20%  
Portfolio Value: 1.001971  

---

## 9. Running Tests

Run all unit tests:
pytest
Check test coverage:
pip3 install pytest-cov
pytest --cov=src tests/

Test Coverage Includes:
Portfolio return calculation
Online state updates
Drawdown logic
Tail event detection
Reservoir sampling
Data processing functions
State persistence
Output formatting

---

## 10. Reproducibility

The system saves its state in:
data/state.json
This allows the program to continue from previous runs.
To reset and start fresh:
rm -f data/state.json
python3 main.py
A fixed random seed is used to ensure reproducible reservoir sampling behavior.
⚠️ Note: Market data is live, so exact returns may vary.

---

## 11. Methodology

This project applies several important data science and systems concepts:
Online Statistics:
Instead of storing full history, statistics are updated incrementally:
- Running mean
- Running variance
- Running volatility

Rolling Window Analysis:
Maintains a fixed-size window of recent returns to track short-term behavior.

Reservoir Sampling
Maintains a fixed-size random sample from a growing data stream.

Drawdown Monitoring:
Tracks:
- Running peak portfolio value
- Current drawdown
- Maximum drawdown

---

## 12. Why This Project Matters

Traditional portfolio analysis relies on full historical datasets and batch computation.
This project demonstrates how streaming algorithms can be used for:
- Real-time financial monitoring
- Memory-efficient computation
- Continuous system updates

---

## 13. Future Improvements

- Add command-line arguments (custom assets & weights)
- Add visualization dashboard
- Add advanced risk metrics (VaR, CVaR)
- Support intraday data
- Replace print with structured logging
- Deploy as a real-time service

---

## 14. Author

Zimo Wu
