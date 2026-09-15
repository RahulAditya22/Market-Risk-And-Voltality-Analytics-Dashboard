# Market Risk & Volatility Analytics Dashboard — Requirements

## 1. Problem statement

Build a focused financial-market analytics application that analyzes historical market behavior and quantifies market risk. The dashboard is not a trading strategy backtester and does not make investment recommendations. It presents historical prices, returns, volatility, drawdown, Value at Risk (VaR), Expected Shortfall (CVaR), correlations, and an explainable volatility regime classification.

The project complements the Multi-Asset Backtesting Engine by emphasizing market analysis and risk measurement rather than strategy evaluation.

## 2. Target user

Primary users are students, quantitative-finance learners, market analysts, and recruiters reviewing evidence of financial-market understanding, statistical reasoning, data engineering, Python, and production software practices.

## 3. Functional requirements

### Asset and period selection
- Provide a curated universe of liquid instruments: Gold, Crude Oil, S&P 500, Nasdaq, EUR/USD, and USD/INR.
- Use verified Yahoo Finance symbols; symbols must be validated during implementation rather than assumed.
- Allow selection of one primary asset.
- Allow an optional comparison asset.
- Allow start and end dates.
- Allow rolling-volatility window selection.
- Allow VaR confidence selection.

### Market analytics
For validated historical price data, calculate:
- current/last available price;
- daily percentage returns;
- rolling volatility;
- annualized volatility using a 252-trading-day convention;
- maximum drawdown;
- historical VaR;
- Expected Shortfall / CVaR;
- downside volatility;
- return distribution;
- Pearson return correlation for aligned assets;
- rolling return correlation;
- rule-based volatility regime.

### Visualization
Display:
- price history;
- rolling volatility;
- return distribution with VaR threshold;
- drawdown;
- correlation matrix when multiple assets are selected;
- rolling correlation when a comparison asset is selected;
- concise interpretation for major risk measures.

### User-facing failure handling
- Live data failures must produce a clear user-facing message.
- The application must not expose a Python traceback to normal users.
- Empty, malformed, or insufficient market data must be rejected or reported clearly.
- The application must never fabricate market data.
- If intentional demo/fallback data is ever added, it must be explicitly labelled as such.

## 4. Non-functional requirements

- Use a clean `src/` package layout with one consistent import strategy.
- The same import assumptions must work locally, in CI, in Streamlit, and on Render.
- Financial calculation functions should be pure and DataFrame-driven wherever practical.
- Keep the Streamlit entry point focused on presentation and orchestration rather than financial logic.
- Prefer small, testable functions with clear contracts.
- Use deterministic tests and fixtures.
- Target at least 80% meaningful test coverage, with higher coverage for financial calculations.
- Use Ruff and Black for quality enforcement.
- Pin direct runtime and development dependencies.
- Keep deployment and CI configuration reproducible.

## 5. Data requirements

The external data source is Yahoo Finance through `yfinance` for historical market data. External access is allowed for the application, but is never required by unit tests.

The data pipeline is:

`external source → data loader → validation → returns → risk analytics → visualization/UI`

Validation must explicitly check required price columns, a DatetimeIndex, chronological ordering, duplicate timestamps, missing values, positive numeric prices, and sufficient observations.

Data must be normalized to a predictable internal representation before financial calculations run.

## 6. Risk metrics

The implementation must document and test:
- simple percentage returns;
- annualized volatility;
- maximum drawdown;
- historical VaR with an explicit confidence/sign convention;
- Expected Shortfall with an explicit threshold rule;
- downside volatility;
- Pearson correlation on returns;
- rolling volatility and rolling correlation;
- rule-based volatility regime.

The UI must explain what each displayed statistic means, how it is calculated, what high/low values imply, and material limitations.

## 7. UI requirements

The Streamlit dashboard should be professional and finance-oriented.

Header:
- title: `Market Risk & Volatility Analytics`;
- subtitle explaining historical market behavior, volatility, and downside risk.

Sidebar:
- asset;
- start date;
- end date;
- volatility window;
- VaR confidence;
- optional comparison asset.

Main content:
- KPI row for current price, latest daily return, annualized volatility, maximum drawdown, and VaR;
- price chart;
- rolling volatility chart;
- return distribution / VaR visualization;
- drawdown chart;
- correlation / rolling correlation section when applicable;
- risk interpretation and regime classification.

Include: `Educational / analytical use only. Not financial advice.`

Do not provide buy/sell recommendations or price predictions.

## 8. Testing requirements

Tests must be deterministic and must not call Yahoo Finance.

The suite must cover normal calculations and important edge cases including empty data, one-row data, insufficient observations, NaNs, duplicate timestamps, unsorted timestamps, invalid prices, constant prices, zero volatility, negative returns, all-positive returns, extreme returns, VaR quantiles, Expected Shortfall, drawdown, correlation, and rolling calculations.

External-data behavior must be tested through mocks for success, empty responses, exceptions, and rate limiting. Tests must verify the application's defined failure behavior rather than relying on live provider behavior.

A Streamlit import/startup smoke test must verify that the application can start under the same logical package/import assumptions used in deployment without requiring live data.

CI must enforce Ruff, Black, tests, coverage, and the startup smoke test.

## 9. Deployment requirements

Deployment target: Render web service running Streamlit.

Before deployment, validate the production-style start command locally. Python version, dependency versions, package imports, working-directory assumptions, port handling, and host binding must be consistent between local validation, CI, and Render.

Render auto-deploy may be enabled only after the repository is known-good. Deployment must be a controlled step rather than a source of repeated experimental deployments.

A deployment is not considered successful until the live service has been checked for startup, UI rendering, data loading, charts, metrics, control changes, and graceful no-data/error handling.

## 10. Security requirements

- No API keys or credentials are required unless a future scope change explicitly introduces them.
- Never commit secrets, tokens, credentials, `.env` files, local caches, or generated artifacts.
- Review `.gitignore` and repository contents before final push and before completion.
- Do not put secrets in screenshots, tests, documentation, YAML, or Git history.

## 11. Explicit project scope

In scope:
- historical market-data retrieval;
- deterministic data validation;
- returns and volatility analytics;
- drawdown;
- historical VaR;
- Expected Shortfall / CVaR;
- downside volatility;
- return distributions;
- multi-asset return correlation;
- rolling correlation;
- simple rule-based volatility regimes;
- Streamlit visualization;
- automated testing;
- CI/CD quality gates;
- Render deployment;
- concise technical and financial documentation.

## 12. Explicit out-of-scope items

- machine-learning price prediction;
- automated trading;
- another strategy backtesting engine;
- live trading execution;
- investment recommendations;
- portfolio optimization;
- options pricing or other derivatives pricing models unless later justified by a separately approved scope change;
- scheduled screenshot pipelines;
- scheduled CI workflows;
- email, Slack, webhook, or other notification automation;
- unnecessary external services.

## 13. Validation gates

No major stage may proceed while its predecessor is failing:

`Audit → Requirements → Architecture → Implementation Plan → Skeleton → Unit Tests → Implementation → Integration Tests → Static Analysis/Formatting → CI → Local Streamlit Smoke Test → Deployment Configuration → Deployment → Live Test → Documentation → Final Audit`

If a failure occurs, capture the exact error, identify the root cause, fix the underlying issue, then rerun the smallest relevant test, the full suite, quality checks, and startup smoke test before continuing.
