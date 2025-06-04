# """Processor module for trend analysis using ADX, Parabolic SAR, and MA crossovers."""

# import pandas as pd
# from ta.trend import ADXIndicator, PSARIndicator

# from app.logger import setup_logger

# # Initialize logger
# logger = setup_logger(__name__)


# def analyze_trend(data: pd.DataFrame) -> pd.DataFrame:
#     """
#     Analyzes stock trends using ADX, Parabolic SAR, and Moving Average Crossovers.

#     Adds the following indicators:
#     - ADX, +DI, -DI
#     - Parabolic SAR
#     - SMA and EMA crossovers
#     - Trend strength classification

#     Args:
#     ----
#         data (pd.DataFrame): Stock data with columns ['High', 'Low', 'Close'].

#     Returns:
#     -------
#         pd.DataFrame: Original data with trend indicators and signals added.
#     """
#     try:
#         required_cols = {"High", "Low", "Close"}
#         if not required_cols.issubset(data.columns):
#             logger.error("Missing one or more required columns: %s", required_cols)
#             return pd.DataFrame()

#         # ADX Calculation
#         adx = ADXIndicator(high=data["High"], low=data["Low"], close=data["Close"], window=14)
#         data["ADX"] = adx.adx()
#         data["+DI"] = adx.adx_pos()
#         data["-DI"] = adx.adx_neg()

#         # Parabolic SAR
#         psar = PSARIndicator(high=data["High"], low=data["Low"], close=data["Close"])
#         data["Parabolic_SAR"] = psar.psar()

#         # SMA Crossover
#         data["SMA_20"] = data["Close"].rolling(window=20).mean()
#         data["SMA_50"] = data["Close"].rolling(window=50).mean()
#         data["SMA_Crossover_Signal"] = (
#             (data["SMA_20"] > data["SMA_50"]).astype(int).replace({0: -1})
#         )

#         # EMA Crossover
#         data["EMA_12"] = data["Close"].ewm(span=12, adjust=False).mean()
#         data["EMA_26"] = data["Close"].ewm(span=26, adjust=False).mean()
#         data["EMA_Crossover_Signal"] = (
#             (data["EMA_12"] > data["EMA_26"]).astype(int).replace({0: -1})
#         )

#         # Trend Strength
#         data["Trend_Strength"] = data["ADX"].apply(classify_trend_strength)

#         logger.info("Successfully computed trend indicators.")
#         return data

#     except Exception as e:
#         logger.error(f"Trend analysis failed: {e}")
#         return pd.DataFrame()


# def classify_trend_strength(adx_value: float) -> str:
#     """
#     Classifies trend strength based on ADX value.

#     Args:
#     ----
#         adx_value (float): ADX value.

#     Returns:
#     -------
#         str: 'Weak', 'Moderate', or 'Strong'
#     """
#     if pd.isna(adx_value):
#         return "Unknown"
#     if adx_value < 20:
#         return "Weak"
#     elif 20 <= adx_value < 40:
#         return "Moderate"
#     else:
#         return "Strong"
"""Processor module for trend analysis using ADX, Parabolic SAR, and MA
crossovers.
"""

from typing import cast

import pandas as pd
from pandas import Series
from ta.trend import ADXIndicator, PSARIndicator

from app.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)


def analyze_trend(data: pd.DataFrame) -> pd.DataFrame:
    """Analyzes stock trends using ADX, Parabolic SAR, and Moving Average
    Crossovers.
    
    Adds the following indicators:
    - ADX, +DI, -DI
    - Parabolic SAR
    - SMA and EMA crossovers
    - Trend strength classification
    
    Args:
    ----
      data(pd.DataFrame): Stock data with columns ['High', 'Low', 'Close'].
      data: pd.DataFrame:
      data: pd.DataFrame:
      data: pd.DataFrame:

    :param data: pd.DataFrame:
    :param data: pd.DataFrame:
    :param data: pd.DataFrame:
    :param data: type data: pd.DataFrame :
    :param data: type data: pd.DataFrame :
    :param data: pd.DataFrame:
    :param data: pd.DataFrame:
    :param data: pd.DataFrame: 

    """
    try:
        required_cols = {"High", "Low", "Close"}
        if not required_cols.issubset(data.columns):
            logger.error("Missing one or more required columns: %s", required_cols)
            return pd.DataFrame()

        high: Series = cast(Series, data["High"])
        low: Series = cast(Series, data["Low"])
        close: Series = cast(Series, data["Close"])

        # ADX Calculation
        adx = ADXIndicator(high=high, low=low, close=close, window=14)
        data["ADX"] = adx.adx()
        data["+DI"] = adx.adx_pos()
        data["-DI"] = adx.adx_neg()

        # Parabolic SAR
        psar = PSARIndicator(high=high, low=low, close=close)
        data["Parabolic_SAR"] = psar.psar()

        # SMA Crossover
        data["SMA_20"] = close.rolling(window=20).mean()
        data["SMA_50"] = close.rolling(window=50).mean()
        data["SMA_Crossover_Signal"] = (
            (data["SMA_20"] > data["SMA_50"]).astype(int).replace({0: -1})
        )

        # EMA Crossover
        data["EMA_12"] = close.ewm(span=12, adjust=False).mean()
        data["EMA_26"] = close.ewm(span=26, adjust=False).mean()
        data["EMA_Crossover_Signal"] = (
            (data["EMA_12"] > data["EMA_26"]).astype(int).replace({0: -1})
        )

        # Trend Strength
        data["Trend_Strength"] = data["ADX"].apply(classify_trend_strength)

        logger.info("Successfully computed trend indicators.")
        return data

    except Exception as e:
        logger.error(f"Trend analysis failed: {e}")
        return pd.DataFrame()


def classify_trend_strength(adx_value: float) -> str:
    """Classifies trend strength based on ADX value.
    
    Args:
    ----
      adx_value(float): ADX value.
      adx_value: float:
      adx_value: float:
      adx_value: float:

    :param adx_value: float:
    :param adx_value: float:
    :param adx_value: float:
    :param adx_value: type adx_value: float :
    :param adx_value: type adx_value: float :
    :param adx_value: float:
    :param adx_value: float:
    :param adx_value: float: 

    """
    if pd.isna(adx_value):
        return "Unknown"
    if adx_value < 20:
        return "Weak"
    elif 20 <= adx_value < 40:
        return "Moderate"
    else:
        return "Strong"
