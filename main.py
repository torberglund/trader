import argparse
import os
from trading_bot import TradingBot


def main():
    parser = argparse.ArgumentParser(description="Trading Bot CLI")
    subparsers = parser.add_subparsers(dest="command")

    trade_parser = subparsers.add_parser(
        "trade", help="Execute a trading strategy"
    )
    trade_parser.add_argument(
        "--strategy",
        required=True,
        choices=["ma", "rsi_bb", "breakout", "ema", "combo"],
    )
    trade_parser.add_argument("--symbol", required=True)
    trade_parser.add_argument("--amount", required=True, type=float)

    subparsers.add_parser("positions", help="Show open positions")

    close_parser = subparsers.add_parser("close", help="Close a position")
    close_parser.add_argument("--symbol", required=True)

    args = parser.parse_args()

    api_key = os.getenv("APCA_API_KEY_ID")
    secret_key = os.getenv("APCA_API_SECRET_KEY")
    base_url = os.getenv(
        "APCA_API_BASE_URL", "https://paper-api.alpaca.markets"
    )

    if not api_key or not secret_key:
        parser.error("API credentials not set in environment variables")

    bot = TradingBot(api_key, secret_key, base_url)

    if args.command == "trade":
        bot.run_strategy(args.strategy, args.symbol, args.amount)
    elif args.command == "positions":
        bot.show_positions()
    elif args.command == "close":
        bot.close_position(args.symbol)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
