from fastapi import FastAPI

from Backend.live_trading import LiveTrading

app = FastAPI()


# what needs to be given? currently nothing just needs to run it. so i guess on startup should just run the task.
@app.on_event("startup")
async def startup_event():
    print("--------------Starting-----------------")
    cerebro = LiveTrading(capital=10000, symbols=[
        'ETHUSDT', 'ETCUSDT', 'BITUSDT', 'GMTUSDT', 'OPUSDT', 'RUNEUSDT', 'TRBUSDT'], timeframe='15m',)
    cerebro.run()
