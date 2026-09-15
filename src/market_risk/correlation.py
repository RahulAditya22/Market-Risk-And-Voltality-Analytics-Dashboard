from __future__ import annotations

import pandas as pd


def align_returns(first: pd.Series, second: pd.Series) -> pd.DataFrame:
    frame = pd.concat([first.rename("first"), second.rename("second")], axis=1, join="inner")
    return frame.dropna()


def pearson_correlation(first: pd.Series, second: pd.Series) -> float:
    aligned = align_returns(first, second)
    if len(aligned) < 2:
        raise ValueError("At least two aligned observations are required for correlation.")
    if aligned["first"].nunique() < 2 or aligned["second"].nunique() < 2:
        raise ValueError("Correlation is undefined for a constant return series.")
    return float(aligned["first"].corr(aligned["second"], method="pearson"))


def correlation_matrix(returns: pd.DataFrame) -> pd.DataFrame:
    clean = returns.dropna(how="all").copy()
    if clean.shape[1] < 2:
        raise ValueError("At least two assets are required for a correlation matrix.")
    return clean.corr(method="pearson")


def rolling_correlation(first: pd.Series, second: pd.Series, window: int = 21) -> pd.Series:
    if window < 2:
        raise ValueError("Correlation window must be at least 2.")
    aligned = align_returns(first, second)
    return aligned["first"].rolling(window).corr(aligned["second"])
