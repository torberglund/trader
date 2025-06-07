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

## Manual

### Installation

1. Ensure you have **Python 3.10+** installed.
2. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install the required dependencies:

   ```bash
   pip install alpaca-trade-api pandas numpy
   ```

### Configuration

The bot requires Alpaca API credentials. Export them in your shell before running
any commands:

```bash
export APCA_API_KEY_ID="<your key>"
export APCA_API_SECRET_KEY="<your secret>"
export APCA_API_BASE_URL="https://paper-api.alpaca.markets"  # optional
```

By default the bot uses Alpaca's paper trading endpoint, which allows you to
test strategies without risking real money.

### Command Reference

Run `python main.py <command>` with one of the following commands:

- `trade` – Execute a strategy.
  - Required flags:
    - `--strategy` one of `ma`, `rsi_bb`, `breakout`, `ema`.
    - `--symbol` the instrument to trade (e.g. `BTCUSD`).
    - `--amount` capital in USD to allocate.
- `positions` – Display all open positions.
- `close` – Close a position. Requires `--symbol`.

### Strategy Descriptions

| Name      | Flag      | Description                                        |
|-----------|-----------|----------------------------------------------------|
| Moving Average Crossover | `ma` | Buys when a short-term moving average crosses above a long-term average and sells on the opposite cross. |
| RSI + Bollinger Bands    | `rsi_bb` | Generates a signal when RSI is overbought or oversold and price touches the Bollinger bands. |
| Intraday Breakout        | `breakout` | Buys on a breakout above the previous day's high or sells below the low. |
| EMA Pullback             | `ema` | Looks for pullbacks to the exponential moving average before entering. |

### Example Usage

```bash
# Trade 100 USD of BTC using the moving average crossover strategy
python main.py trade --strategy ma --symbol BTCUSD --amount 100

# View current positions
python main.py positions

# Close the BTC position
python main.py close --symbol BTCUSD
```

### Tips

- Start with paper trading to familiarise yourself with order execution.
- You can tweak strategy parameters in `strategies.py` to experiment with
  different indicators or time frames.
- Review Alpaca's documentation for more API features and order options.

### Running Tests

Unit tests are located in the `tests/` directory and can be run with `pytest`:

```bash
pip install pytest
pytest
```

Running the tests is optional for normal usage but recommended when modifying
the code.
