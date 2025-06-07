import os
import pandas as pd
from alpaca_trade_api import REST
from strategies import (
    ma_crossover_signal,
    rsi_bollinger_signal,
    breakout_signal,
    ema_pullback_signal,
    combined_signal,
    TradeSignal,
)


class TradingBot:
    """Simple trading bot using Alpaca API."""

    def __init__(
        self,
        api_key: str,
        secret_key: str,
        base_url: str = "https://api.alpaca.markets",
    ):
        self.api = REST(api_key, secret_key, base_url, api_version="v2")
        self.positions = {}

    def fetch_data(
        self, symbol: str, timeframe: str = "15Min", limit: int = 200
    ) -> pd.DataFrame:
        bars = self.api.get_crypto_bars(symbol, timeframe, limit=limit).df
        return bars[bars["symbol"] == symbol]

    def place_order(self, symbol: str, qty: float, side: str):
        order = self.api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type="market",
            time_in_force="gtc",
        )
        self.positions[symbol] = order.id
        print(f"Submitted {side} order for {qty} {symbol}")
        return order

    def close_position(self, symbol: str):
        try:
            self.api.close_position(symbol)
            self.positions.pop(symbol, None)
            print(f"Closed position in {symbol}")
        except Exception as e:
            print(f"Error closing position: {e}")

    def show_positions(self):
        positions = self.api.list_positions()
        for p in positions:
            print(
                f"{p.symbol} qty={p.qty} side={p.side} unrealized_pl={p.unrealized_pl}"
            )

    def run_strategy(self, strategy: str, symbol: str, capital: float):
        df = self.fetch_data(symbol)
        signal = None
        if strategy == "ma":
            signal = ma_crossover_signal(df)
        elif strategy == "rsi_bb":
            signal = rsi_bollinger_signal(df)
        elif strategy == "breakout":
            signal = breakout_signal(df)
        elif strategy == "ema":
            signal = ema_pullback_signal(df)
        elif strategy == "combo":
            signal = combined_signal(df)
        else:
            print(f"Unknown strategy {strategy}")
            return
        if signal:
            price = df["close"].iloc[-1]
            qty = capital / price
            side = "buy" if signal.action == "buy" else "sell"
            self.place_order(symbol, qty, side)
            if signal.stop:
                print(f"Suggested stop loss: {signal.stop:.2f}")
            if signal.target:
                print(f"Suggested take profit: {signal.target:.2f}")
        else:
            print("No trading signal generated")
