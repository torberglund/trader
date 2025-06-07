# Trading Bot

This repository contains a minimal command line trading bot that connects to the
Alpaca API. It provides multiple trading strategies and a combined strategy that
aggregates their signals:

- Moving Average Crossover (`ma`)
- RSI with Bollinger Bands (`rsi_bb`)
- Intraday High/Low Breakout (`breakout`)
- EMA Pullback (`ema`)
- Combined strategy using all of the above (`combo`)

The bot is intended for educational use. It defaults to Alpaca's paper trading
endpoint so you can paper trade safely. Each order will print suggested stop
loss and take-profit levels when available. You must set your API credentials in the
environment:

```bash
export APCA_API_KEY_ID="<your key>"
export APCA_API_SECRET_KEY="<your secret>"
# optional: export APCA_API_BASE_URL="https://paper-api.alpaca.markets"
```

Run the bot with the desired command:

```bash
# Execute a strategy with a symbol and amount of capital (USD)
python main.py trade --strategy ma --symbol BTCUSD --amount 100

# Use the combined strategy
python main.py trade --strategy combo --symbol BTCUSD --amount 100

# Show open positions
python main.py positions

# Close a position
python main.py close --symbol BTCUSD
```

The code is simplified and does not include advanced risk management. Use at
your own risk and review the source before trading with real money.
