import ccxt

from .config import APIkey, APIsecret

EXCHANGE = ccxt.bybit(
    {
        "apiKey": APIkey,
        "secret": APIsecret,
        "options": {
            "recvWindow": 10000,
            "adjustForTimeDifference": True,
        },
        "enableRateLimit": True,
        # 'verbose': True
    }
)
