from setuptools import setup, find_packages

setup(
    name="streaming_portfolio_monitor",
    version="0.1.0",
    description="A streaming portfolio monitoring system using online statistics and reservoir sampling.",
    packages=find_packages(),
    install_requires=[
        "yfinance",
        "pandas",
        "numpy",
    ],
)