from __future__ import annotations

from dataclasses import dataclass
import pandas as pd
import numpy as np


@dataclass
class TradeSignal:
    """Represents a trading signal with optional risk parameters."""

    action: str
    stop: float | None = None
    target: float | None = None


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Compute the Average True Range."""
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(period).mean()


def ma_crossover_signal(
    df: pd.DataFrame, short: int = 20, long: int = 50
) -> TradeSignal | None:
    df["short_ma"] = df["close"].rolling(short).mean()
    df["long_ma"] = df["close"].rolling(long).mean()
    if len(df) < long + 1:
        return None
    if (
        df["short_ma"].iloc[-1] > df["long_ma"].iloc[-1]
        and df["short_ma"].iloc[-2] <= df["long_ma"].iloc[-2]
    ):
        stop = df["long_ma"].iloc[-1]
        return TradeSignal("buy", stop=stop)
    if (
        df["short_ma"].iloc[-1] < df["long_ma"].iloc[-1]
        and df["short_ma"].iloc[-2] >= df["long_ma"].iloc[-2]
    ):
        stop = df["long_ma"].iloc[-1]
        return TradeSignal("sell", stop=stop)
    return None


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = -delta.clip(upper=0).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def rsi_bollinger_signal(
    df: pd.DataFrame, rsi_low: int = 30, rsi_high: int = 70, period: int = 20
) -> TradeSignal | None:
    df["rsi"] = rsi(df["close"])
    ma = df["close"].rolling(period).mean()
    std = df["close"].rolling(period).std()
    df["upper"] = ma + 2 * std
    df["lower"] = ma - 2 * std
    last = df.iloc[-1]
    if last["rsi"] < rsi_low and last["close"] < last["lower"]:
        stop = last["lower"]
        target = ma.iloc[-1]
        return TradeSignal("buy", stop=stop, target=target)
    if last["rsi"] > rsi_high and last["close"] > last["upper"]:
        stop = last["upper"]
        target = ma.iloc[-1]
        return TradeSignal("sell", stop=stop, target=target)
    return None


def breakout_signal(df: pd.DataFrame, buffer: float = 0.001) -> TradeSignal | None:
    """Breakout of prior day's range with ATR-based stops."""

    if len(df) < 2:
        return None

    df = df.copy()
    df["date"] = df.index.date
    today_date = df["date"].iloc[-1]
    prev_df = df[df["date"] < today_date]
    if prev_df.empty:
        return None

    prev_high = prev_df["high"].max()
    prev_low = prev_df["low"].min()

    today_df = df[df["date"] == today_date]
    current_high = today_df["high"].max()
    current_low = today_df["low"].min()

    high_level = max(prev_high, current_high)
    low_level = min(prev_low, current_low)

    atr_val = atr(df).iloc[-1]
    last_close = df["close"].iloc[-1]

    if last_close > high_level * (1 + buffer):
        stop = last_close - 1.5 * atr_val
        target = last_close + 2 * atr_val
        return TradeSignal("buy", stop=stop, target=target)

    if last_close < low_level * (1 - buffer):
        stop = last_close + 1.5 * atr_val
        target = last_close - 2 * atr_val
        return TradeSignal("sell", stop=stop, target=target)

    return None


def ema_pullback_signal(
    df: pd.DataFrame, period: int = 20, trend_bars: int = 3
) -> TradeSignal | None:
    """Trend-continuation pullback entry using a single EMA."""

    df["ema"] = df["close"].ewm(span=period, adjust=False).mean()
    if len(df) < period + trend_bars + 1:
        return None

    atr_val = atr(df).iloc[-1]

    # Determine if market has been above or below EMA for the last few bars
    recent = df.iloc[-(trend_bars + 1) : -1]
    if (recent["close"] > recent["ema"]).all():
        last = df.iloc[-1]
        if last["close"] > last["ema"] and last["low"] <= last["ema"]:
            stop = last["ema"] - atr_val
            return TradeSignal("buy", stop=stop)

    if (recent["close"] < recent["ema"]).all():
        last = df.iloc[-1]
        if last["close"] < last["ema"] and last["high"] >= last["ema"]:
            stop = last["ema"] + atr_val
            return TradeSignal("sell", stop=stop)

    return None


def combined_signal(df: pd.DataFrame) -> TradeSignal | None:
    """Aggregate signals from all strategies using majority vote."""

    signals = [
        ma_crossover_signal(df),
        rsi_bollinger_signal(df),
        breakout_signal(df),
        ema_pullback_signal(df),
    ]
    actions = [s.action for s in signals if s]
    if not actions:
        return None
    buy_count = actions.count("buy")
    sell_count = actions.count("sell")
    if buy_count == sell_count:
        return None
    action = "buy" if buy_count > sell_count else "sell"

    stops = [s.stop for s in signals if s and s.stop is not None]
    targets = [s.target for s in signals if s and s.target is not None]
    stop = float(np.nanmean(stops)) if stops else None
    target = float(np.nanmean(targets)) if targets else None
    return TradeSignal(action, stop=stop, target=target)
