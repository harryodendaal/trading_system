import ccxt
from .config import APIkey, APIsecret
EXCHANGE = ccxt.bybit({
    'apiKey': APIkey,
    'secret': APIsecret,
    'options': {
        'recvWindow': 10000000,
        'adjustForTimeDifference': True,
    },
    'enableRateLimit': True,
    # 'verbose': True
})

STRATEGIES = ['1', '2']
