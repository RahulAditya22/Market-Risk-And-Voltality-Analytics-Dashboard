# Architecture

## Design goal

Keep external market-data access, validation, financial calculations, plotting, and Streamlit orchestration separate. This prevents provider failures from contaminating the calculation layer and avoids the import/runtime problems encountered in the previous project.

## Runtime flow

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

## Package layout

```text
project-root/
├── app/
│   └── streamlit_app.py
├── src/
│   └── market_risk/
│       ├── __init__.py
│       ├── config.py
│       ├── data_loader.py
│       ├── validation.py
│       ├── returns.py
│       ├── volatility.py
│       ├── risk_metrics.py
│       ├── correlation.py
│       ├── regimes.py
│       └── plotting.py
├── tests/
│   ├── conftest.py
│   ├── fixtures/
│   ├── test_validation.py
│   ├── test_returns.py
│   ├── test_volatility.py
│   ├── test_risk_metrics.py
│   ├── test_correlation.py
│   ├── test_regimes.py
│   ├── test_data_loader.py
│   ├── test_plotting.py
│   └── test_app_smoke.py
├── docs/
├── .github/workflows/ci.yml
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
├── requirements.txt
└── render.yaml
```

## Import strategy

Use a true `src` package layout:

```text
src/market_risk/
```

Application and tests import the installed package as `market_risk`, never as `src.market_risk`. The package is installed through `pyproject.toml` in local development and CI. Render uses the same install step. This deliberately avoids the previous project's fragile split between `src.*` and package imports.

The production start command therefore does not depend on an ad-hoc `PYTHONPATH` assignment.

## Data boundary

`data_loader.py` is the only layer allowed to call `yfinance`. It returns a normalized price DataFrame or a defined data-access error. Calculation modules accept DataFrames/Series supplied by callers and never call the network.

This boundary makes unit tests deterministic and prevents provider rate limits from affecting financial formula tests.

## Validation boundary

All externally sourced price data passes through explicit validation before returns or risk calculations. Validation rejects missing required columns, invalid index types, duplicate timestamps, unsorted timestamps, missing/non-numeric/non-positive prices, and insufficient observations.

## Calculation boundary

Financial calculations are pure functions wherever practical. They use decimal returns internally as standard numerical values and return documented decimal or percentage-compatible values consistently.

## UI boundary

`app/streamlit_app.py` owns Streamlit controls, caching, orchestration, and presentation. It should not contain formulas or provider-specific code. Importing the module for smoke tests must not trigger a network request. Live data retrieval starts only after the user explicitly clicks **Run analysis**.

## Caching

Cache only the external data retrieval function with a short TTL. User-selected date ranges and analytics are calculated from the selected validated data on each rerun so cached results cannot become stale across control changes.

## Deployment architecture

Render runs the same Python package installation used in CI, then starts Streamlit on `0.0.0.0:$PORT`. Python version is pinned consistently in the project, CI, and Render configuration. The production-style command is tested locally before deployment.

## Failure behavior

```text
Yahoo Finance
   │
   ├── success → normalize → validate → calculate → render
   │
   ├── empty/malformed → defined data error → user-facing message
   │
   └── exception/rate limit → defined data error → user-facing message
```

No synthetic data is silently substituted for a live-data failure.

## No-lookahead discipline

Rolling metrics use observations available at or before each timestamp. The application is analytical rather than a backtester, but historical rolling statistics must still avoid future observations when interpreted through time.
