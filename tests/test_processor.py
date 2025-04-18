"""
Test suite for trend analysis processor.
"""

import pandas as pd

from app.processor import analyze_trend_indicators


def generate_test_data() -> pd.DataFrame:
    """
    Generates mock OHLC test data for trend analysis.

    Returns:
        pd.DataFrame: OHLC stock data with 'symbol' and 'timestamp'.
    """
    return pd.DataFrame(
        {
            "High": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            "Low": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
            "Close": [7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
            "Open": [6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            "symbol": ["TEST"] * 10,
            "timestamp": pd.date_range(start="2024-01-01", periods=10, freq="D").astype(str),
        }
    )


def test_adx_analysis():
    """
    Validates that the ADX indicator is calculated and returned.
    """
    df = generate_test_data()
    result = analyze_trend_indicators(df, window=5)

    assert "ADX" in result["trend"].iloc[0]
    assert isinstance(result["trend"].iloc[0]["ADX"], float)


def test_parabolic_sar_analysis():
    """
    Validates that the Parabolic SAR value is calculated.
    """
    df = generate_test_data()
    result = analyze_trend_indicators(df, window=5)

    assert "ParabolicSAR" in result["trend"].iloc[0]
    assert isinstance(result["trend"].iloc[0]["ParabolicSAR"], float)


def test_ma_crossover_analysis():
    """
    Validates that the moving average crossover signal is detected.
    """
    df = generate_test_data()
    result = analyze_trend_indicators(df, window=3)

    assert "MA_Crossover" in result["trend"].iloc[0]
    assert result["trend"].iloc[0]["MA_Crossover"] in {"Bullish", "Bearish", "No Signal"}
