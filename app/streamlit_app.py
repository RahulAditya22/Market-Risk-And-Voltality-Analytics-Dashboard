from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
import streamlit as st

from market_risk.config import ASSETS, DEFAULT_VAR_CONFIDENCE, DEFAULT_VOLATILITY_WINDOW
from market_risk.correlation import correlation_matrix, rolling_correlation
from market_risk.data_loader import MarketDataError, asset_ticker, fetch_price_data
from market_risk.plotting import (
    correlation_heatmap,
    drawdown_chart,
    price_chart,
    return_distribution_chart,
    rolling_correlation_chart,
    rolling_volatility_chart,
)
from market_risk.regimes import classify_volatility_regime
from market_risk.returns import calculate_returns
from market_risk.risk_metrics import expected_shortfall, historical_var, maximum_drawdown
from market_risk.volatility import annualized_volatility, downside_volatility, rolling_volatility


@st.cache_data(ttl=900, show_spinner=False)
def load_cached(ticker: str, start: date, end: date) -> pd.DataFrame:
    return fetch_price_data(ticker, start, end + timedelta(days=1))


def main() -> None:
    st.set_page_config(page_title="Market Risk & Volatility Analytics", layout="wide")
    st.title("Market Risk & Volatility Analytics")
    st.caption("Analyze historical market behavior, volatility and downside risk.")

    with st.sidebar:
        st.header("Analysis Controls")
        asset_name = st.selectbox("Asset", list(ASSETS))
        comparison = st.selectbox(
            "Comparison asset (optional)",
            ["None", *[asset for asset in ASSETS if asset != asset_name]],
        )
        end_date = st.date_input("End date", value=date.today())
        start_date = st.date_input("Start date", value=end_date - timedelta(days=365 * 3))
        volatility_window = st.slider(
            "Volatility window (days)", 5, 90, DEFAULT_VOLATILITY_WINDOW
        )
        confidence = st.select_slider(
            "VaR confidence",
            options=[0.90, 0.95, 0.99],
            value=DEFAULT_VAR_CONFIDENCE,
            format_func=lambda value: f"{value:.0%}",
        )

    if start_date >= end_date:
        st.error("Start date must be earlier than end date.")
        st.stop()

    try:
        prices = load_cached(asset_ticker(asset_name), start_date, end_date)
        returns = calculate_returns(prices["Close"])
        rolling_vol = rolling_volatility(returns, volatility_window)
        annual_vol = annualized_volatility(returns)
        downside_vol = downside_volatility(returns)
        max_dd = maximum_drawdown(prices["Close"])
        var = historical_var(returns, confidence)
        es = expected_shortfall(returns, confidence)
        regimes = classify_volatility_regime(rolling_vol)
    except (MarketDataError, ValueError) as exc:
        st.error(str(exc))
        st.stop()

    latest_return = float(returns.iloc[-1]) if not returns.empty else float("nan")
    available_regimes = regimes[regimes != "UNAVAILABLE"].dropna()
    latest_regime = available_regimes.iloc[-1] if not available_regimes.empty else "UNAVAILABLE"

    cols = st.columns(5)
    cols[0].metric("Current Price", f"{prices['Close'].iloc[-1]:,.2f}")
    cols[1].metric("Daily Return", f"{latest_return:.2%}")
    cols[2].metric("Annualized Volatility", f"{annual_vol:.2%}")
    cols[3].metric("Maximum Drawdown", f"{max_dd:.2%}")
    cols[4].metric(f"Historical VaR ({confidence:.0%})", f"{var:.2%}")

    st.plotly_chart(
        price_chart(prices["Close"], f"{asset_name} Price History"), use_container_width=True
    )
    st.plotly_chart(
        rolling_volatility_chart(rolling_vol, f"{volatility_window}-Day Rolling Volatility"),
        use_container_width=True,
    )
    st.plotly_chart(return_distribution_chart(returns, var), use_container_width=True)
    st.plotly_chart(drawdown_chart(prices["Close"]), use_container_width=True)

    risk_left, risk_right = st.columns(2)
    with risk_left:
        st.subheader("Risk Summary")
        st.metric("Expected Shortfall", f"{es:.2%}")
        st.metric("Downside Volatility", f"{downside_vol:.2%}")
    with risk_right:
        st.subheader("Risk Regime")
        st.markdown(f"### {latest_regime}")
        st.write(
            "The regime is classified from the selected rolling-volatility series using its "
            "33rd and 67th historical percentiles. It is descriptive, not predictive."
        )

    if comparison != "None":
        try:
            comparison_prices = load_cached(asset_ticker(comparison), start_date, end_date)
            comparison_returns = calculate_returns(comparison_prices["Close"])
            aligned = pd.concat(
                [returns.rename(asset_name), comparison_returns.rename(comparison)],
                axis=1,
                join="inner",
            ).dropna()
            matrix = correlation_matrix(aligned)
            st.subheader("Return Correlation")
            st.plotly_chart(correlation_heatmap(matrix), use_container_width=True)
            rolling_corr = rolling_correlation(returns, comparison_returns, volatility_window)
            st.plotly_chart(rolling_correlation_chart(rolling_corr), use_container_width=True)
        except (MarketDataError, ValueError) as exc:
            st.warning(f"Comparison analysis unavailable: {exc}")

    with st.expander("What do these metrics mean?"):
        st.markdown(
            "- **Volatility:** dispersion of daily returns, annualized using √252.\n"
            "- **Maximum drawdown:** largest percentage decline from a historical peak.\n"
            "- **Historical VaR:** empirical loss threshold for the selected confidence level.\n"
            "- **Expected Shortfall:** average historical loss in observations beyond the VaR threshold.\n"
            "- **Downside volatility:** dispersion of negative returns only.\n"
            "- **Correlation:** Pearson correlation of aligned returns, not raw prices."
        )

    st.caption("Educational / analytical use only. Not financial advice.")


if __name__ == "__main__":
    main()
