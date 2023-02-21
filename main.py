import ccxt
from fastapi import FastAPI

from Backend.strategies.strategy_interface import Strategies
from Backend.trading import Trading

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    """
    The entry point
    """
    print("--------------Starting-----------------")
    print("CCXT Version:", ccxt.__version__)

    symbols = [
        # "ETHUSDT",
        # "ETCUSDT",
        "BITUSDT",
        # "GMTUSDT",
        # "OPUSDT",
        # "RUNEUSDT",
        # "TRBUSDT",
    ]
    trade_size = 10

    # symbols = filter_trading_symbols(symbols, trade_size)

    cerebro = Trading(
        symbols=symbols,
        trade_size=trade_size,
    )
    cerebro.run()


# so modular programming and absolute imports for now nuber one.
