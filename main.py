import ccxt
from fastapi import FastAPI

from live_backend.exchange_interface.live_exchange_interface import (
    filter_trading_symbols,
)
from live_backend.strategies.strategies import Strategies
from live_backend.trading import Trading

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
        "ETCUSDT",
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
