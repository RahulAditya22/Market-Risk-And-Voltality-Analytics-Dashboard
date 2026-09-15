from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def price_chart(prices: pd.Series, title: str) -> go.Figure:
    return px.line(prices, title=title, labels={"value": "Price", "index": "Date"})


def rolling_volatility_chart(rolling_vol: pd.Series, title: str) -> go.Figure:
    return px.line(rolling_vol, title=title, labels={"value": "Volatility", "index": "Date"})


def return_distribution_chart(
    returns: pd.Series, var: float, title: str = "Return Distribution and Historical VaR"
) -> go.Figure:
    fig = px.histogram(returns, nbins=50, title=title, labels={"value": "Daily return"})
    threshold = -var
    fig.add_vline(x=threshold, annotation_text=f"VaR threshold: {threshold:.2%}")
    return fig


def drawdown_chart(prices: pd.Series, title: str = "Historical Drawdown") -> go.Figure:
    drawdown = prices / prices.cummax() - 1.0
    return px.area(drawdown, title=title, labels={"value": "Drawdown", "index": "Date"})


def correlation_heatmap(matrix: pd.DataFrame, title: str = "Return Correlation") -> go.Figure:
    return px.imshow(matrix, text_auto=".2f", zmin=-1, zmax=1, title=title)


def rolling_correlation_chart(
    series: pd.Series, title: str = "Rolling Return Correlation"
) -> go.Figure:
    return px.line(series, title=title, labels={"value": "Correlation", "index": "Date"})
