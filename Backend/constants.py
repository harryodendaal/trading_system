import ccxt
from .config import APIkey, APIsecret
EXCHANGE = ccxt.bybit({
    'apiKey': APIkey,
    'secret': APIsecret,
    'enableRateLimit': True,
    # 'recvWindow': 10000000,
    'adjustForTimeDifference': True
    # 'verbose': True,
})

STRATEGIES = ['1', '2']
