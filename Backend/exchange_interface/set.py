from Backend.exchange_interface.constants import EXCHANGE


def set_leverage(leverage: int, symbol: str):
    EXCHANGE.set_leverage(leverage, symbol)


def set_position_mode_of_exchange(symbol):
    EXCHANGE.set_position_mode(0, symbol=symbol)
