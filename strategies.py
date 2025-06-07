import pandas as pd
import numpy as np


def ma_crossover_signal(
    df: pd.DataFrame, short: int = 20, long: int = 50
) -> str | None:
    df["short_ma"] = df["close"].rolling(short).mean()
    df["long_ma"] = df["close"].rolling(long).mean()
    if len(df) < long + 1:
        return None
    if (
        df["short_ma"].iloc[-1] > df["long_ma"].iloc[-1]
        and df["short_ma"].iloc[-2] <= df["long_ma"].iloc[-2]
    ):
        return "buy"
    if (
        df["short_ma"].iloc[-1] < df["long_ma"].iloc[-1]
        and df["short_ma"].iloc[-2] >= df["long_ma"].iloc[-2]
    ):
        return "sell"
    return None


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = -delta.clip(upper=0).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def rsi_bollinger_signal(
    df: pd.DataFrame, rsi_low: int = 30, rsi_high: int = 70, period: int = 20
) -> str | None:
    df["rsi"] = rsi(df["close"])
    ma = df["close"].rolling(period).mean()
    std = df["close"].rolling(period).std()
    df["upper"] = ma + 2 * std
    df["lower"] = ma - 2 * std
    last = df.iloc[-1]
    if last["rsi"] < rsi_low and last["close"] < last["lower"]:
        return "buy"
    if last["rsi"] > rsi_high and last["close"] > last["upper"]:
        return "sell"
    return None


def breakout_signal(df: pd.DataFrame, buffer: float = 0.001) -> str | None:
    if len(df) < 2:
        return None
    df = df.copy()
    df["date"] = df.index.date
    today = df.iloc[-1]
    prev_day = df[df["date"] < today["date"]].iloc[-1]
    high_level = prev_day["high"]
    low_level = prev_day["low"]
    if today["close"] > high_level * (1 + buffer):
        return "buy"
    if today["close"] < low_level * (1 - buffer):
        return "sell"
    return None


def ema_pullback_signal(df: pd.DataFrame, period: int = 20) -> str | None:
    df["ema"] = df["close"].ewm(span=period, adjust=False).mean()
    if len(df) < period + 2:
        return None
    if (
        df["close"].iloc[-1] > df["ema"].iloc[-1]
        and df["close"].iloc[-2] <= df["ema"].iloc[-2]
    ):
        return "buy"
    if (
        df["close"].iloc[-1] < df["ema"].iloc[-1]
        and df["close"].iloc[-2] >= df["ema"].iloc[-2]
    ):
        return "sell"
    return None
