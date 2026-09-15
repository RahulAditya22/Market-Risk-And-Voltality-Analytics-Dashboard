# Financial Metrics

All calculations operate on validated historical prices and decimal returns. The dashboard explains the interpretation and limitations of each metric rather than presenting unexplained numbers.

## Returns

For price `P_t`:

`r_t = P_t / P_(t-1) - 1`

The first observation has no prior price and therefore produces no return.

## Rolling volatility

For a rolling window of `w` daily returns:

`rolling_vol_t = std(r_(t-w+1)...r_t)`

The sample standard deviation (`ddof=1`) is used when enough observations exist. This is a historical realized-volatility measure, not an implied-volatility estimate.

## Annualized volatility

Using 252 trading days:

`annualized_vol = std(daily_returns) × sqrt(252)`

The result is expressed as a decimal; the UI formats it as a percentage.

## Maximum drawdown

Define the running peak:

`peak_t = max(P_1...P_t)`

Then:

`drawdown_t = P_t / peak_t - 1`

Maximum drawdown is the minimum value of the drawdown series. It represents the largest historical percentage decline from a previous peak to a subsequent trough.

## Historical VaR

For confidence level `α`, historical VaR uses the empirical lower-tail return quantile at probability `1 - α`.

The application reports VaR as a **positive loss magnitude**:

`VaR_α = -quantile(returns, 1 - α)`

when the lower-tail quantile is negative. If the historical lower-tail quantile is positive, the loss magnitude is reported as zero because the selected historical sample contains no loss at that threshold.

Interpretation: at the selected confidence level, historical VaR estimates a loss threshold that was exceeded by the worst `(1 - α) × 100%` of historical returns under this empirical methodology.

Limitations: VaR does not describe the average size of losses beyond the threshold, and historical VaR depends on the sample period and cannot guarantee future losses.

## Expected Shortfall / CVaR

Expected Shortfall is the mean return of observations in the historical lower tail at or beyond the VaR return threshold. The application reports the corresponding positive loss magnitude:

`ES_α = -mean(r_t | r_t <= q_(1-α))`

If the historical tail contains no negative loss, the reported loss magnitude is zero.

Interpretation: Expected Shortfall estimates the average loss among observations in the selected worst historical tail.

Limitations: it is sample-dependent and sensitive to the number of observations and the historical distribution.

## Downside volatility

Downside volatility measures dispersion of negative returns relative to a zero-return target. Positive returns are not counted as downside observations. The sample standard deviation is used when at least two downside observations are available; otherwise the metric is zero when no meaningful downside dispersion can be estimated.

This is a risk-focused dispersion measure and should not be interpreted as total volatility.

## Pearson correlation

For two aligned return series `X` and `Y`:

`ρ = cov(X, Y) / (σ_X σ_Y)`

Correlation is calculated on returns, **not raw prices**, after timestamp alignment. A value near +1 indicates strong positive linear co-movement; near -1 indicates strong negative linear co-movement; near 0 indicates weak linear co-movement.

Correlation is not causation and can change materially across market regimes.

## Rolling correlation

Rolling correlation applies Pearson correlation to a moving window of aligned return observations. It uses only observations available through each timestamp, preserving time-series integrity.

## Volatility regime

The regime classifier is intentionally rule-based and explainable. For a rolling volatility series, calculate historical quantiles using the selected analysis sample:

- **LOW VOLATILITY:** rolling volatility at or below the 33rd percentile;
- **MEDIUM VOLATILITY:** above the 33rd percentile and at or below the 67th percentile;
- **HIGH VOLATILITY:** above the 67th percentile.

The dashboard labels the latest available regime and explains the rule. This is a descriptive classification, not a prediction.

## Data conventions and limitations

- Returns are decimals internally and percentages only at presentation boundaries.
- Annualization uses 252 trading days.
- NaNs created by lagging or rolling windows are excluded only where the metric mathematically requires complete observations.
- Insufficient observations produce an explicit error or unavailable metric rather than a fabricated value.
- Timestamps are aligned before multi-asset statistics.
- Rolling statistics never use future observations.
