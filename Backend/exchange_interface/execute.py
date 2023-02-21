from Backend.exchange_interface.constants import EXCHANGE


def open_position(symbol, side, amount):
    return EXCHANGE.create_order(symbol, "market", side, amount)


def close_position(symbol, side, amount):
    return EXCHANGE.create_order(
        symbol, "market", side, amount=amount, params={"reduce_only": True}
    )
