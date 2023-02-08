from fastapi import FastAPI
import ccxt
from LIVE.live_trading import LiveTrading

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print("--------------Starting-----------------")
    print('CCXT Version:', ccxt.__version__)
    cerebro = LiveTrading(capital=10000, symbols=[
        'ETHUSDT', 'ETCUSDT', 'BITUSDT', 'GMTUSDT', 'OPUSDT', 'RUNEUSDT', 'TRBUSDT'], timeframe='15m', strategy=3, trade_size=10)
    cerebro.run()


# so modular programming and absolute imports for now nuber one.