# Market Risk & Volatility Analytics Dashboard

[![CI](https://github.com/RahulAditya22/Market-Risk-And-Voltality-Analytics-Dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/RahulAditya22/Market-Risk-And-Voltality-Analytics-Dashboard/actions/workflows/ci.yml)

## Overview

A focused financial-market analytics application for analyzing historical market behavior and quantifying downside risk. It separates market-data acquisition from deterministic financial calculations and presents volatility, drawdown, Value at Risk, Expected Shortfall, correlations, and an explainable volatility regime in a Streamlit dashboard.

The repository name intentionally retains the existing spelling `Voltality`; application code and documentation use the correct spelling **Volatility**.

## Why this project?

This project complements the Multi-Asset Backtesting Engine. The backtesting project focuses on strategy evaluation; this project focuses on market behavior and risk measurement.

It demonstrates:

- financial-market understanding;
- statistical and time-series analysis;
- risk measurement;
- Python, Pandas, and NumPy;
- data validation and engineering;
- professional visualization;
- deterministic automated testing;
- CI quality gates;
- production deployment practices.

## Features

- curated market universe: Gold, Crude Oil, S&P 500, Nasdaq, EUR/USD, USD/INR;
- historical price analysis;
- daily returns;
- rolling and annualized volatility;
- maximum drawdown;
- historical VaR;
- Expected Shortfall / CVaR;
- downside volatility;
- return distributions;
- multi-asset return correlation;
- rolling correlation;
- rule-based low/medium/high volatility regimes;
- explicit user-controlled live-data retrieval;
- graceful market-data failure handling;
- finance-oriented Streamlit interface.

## Risk Metrics

The dashboard documents the mathematical definition and interpretation of every major statistic in [`docs/financial_metrics.md`](docs/financial_metrics.md).

Key conventions include:

- returns: `P_t / P_(t-1) - 1`;
- annualized volatility: daily return standard deviation × `sqrt(252)`;
- maximum drawdown: largest percentage decline from a historical peak;
- historical VaR: empirical lower-tail return quantile reported as a positive loss magnitude;
- Expected Shortfall: average loss in observations at or beyond the VaR threshold;
- correlation: Pearson correlation of aligned returns, never raw prices;
- rolling statistics: only information available through the relevant timestamp is used.

## Data Source

Historical market data is retrieved from Yahoo Finance through `yfinance`. The configured symbols were verified against Yahoo Finance before implementation:

| Asset | Yahoo Finance symbol |
|---|---|
| Gold | `GC=F` |
| Crude Oil | `CL=F` |
| S&P 500 | `^GSPC` |
| Nasdaq | `^IXIC` |
| EUR/USD | `EURUSD=X` |
| USD/INR | `USDINR=X` |

External market data is never required for unit tests.

## Architecture

```text
User
  ↓
Streamlit UI
  ↓
Data Loader
  ↓
Validation
  ↓
Returns
  ↓
Risk Analytics
  ↓
Visualization
```

The calculation layer operates entirely on supplied DataFrames/Series. Yahoo Finance access is isolated to the data-loader boundary. See [`docs/architecture.md`](docs/architecture.md).

## Tech Stack

- Python 3.13
- Pandas
- NumPy
- yfinance
- Plotly
- Streamlit
- Pytest / pytest-cov
- Ruff
- Black
- GitHub Actions
- Render

Dependencies are pinned in `requirements.txt` and the Python version is kept consistent across local/CI/Render configuration.

## Testing

The test suite uses deterministic data and mocks the external Yahoo Finance boundary. It covers validation failures, returns, volatility, drawdown, VaR, Expected Shortfall, correlation, rolling calculations, regimes, provider failures, response normalization, and visualization construction.

CI enforces:

1. Ruff;
2. Black;
3. Pytest with 80% minimum coverage;
4. Streamlit import/startup smoke validation.

See [`docs/testing.md`](docs/testing.md).

## Deployment

The application is configured for Render with a Python web service and Streamlit start command. Deployment validation is deliberately controlled: the repository must pass local/CI quality gates before a production deployment is treated as valid.

**Deployment status:** pending final CI and live-service verification.

## Screenshots

Screenshots are documentation assets and will be added only after the live application has been validated. No screenshot workflow runs on normal pushes.

## Limitations

- historical analysis depends on the availability and quality of Yahoo Finance data;
- historical risk metrics are sample-dependent;
- VaR does not describe the size of losses beyond its threshold;
- correlation measures linear co-movement and can change across regimes;
- the volatility regime is descriptive, not predictive;
- the application is not a trading system or investment recommendation engine.

## Future Improvements

Potential future extensions, subject to scope control, include additional validated instruments, richer stress scenarios, more robust data-source abstraction, and deeper derivatives-oriented risk analytics where justified.

Machine-learning price prediction, automated trading, and another strategy backtester are intentionally outside the current scope.

## Disclaimer

Educational / analytical use only. Not financial advice.
