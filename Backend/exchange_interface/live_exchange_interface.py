# TODO organize this file and break into different submodules
from typing import List

from Backend.exchange_interface import execute, fetch, set
from Backend.exchange_interface.constants import EXCHANGE


def go_trade(action: str, trade_size: int, symbol: str):
    """
    takes the action, size and symbol
    opens a position
    :param action: whether open short or long
    :param size: the dollar amount you, want to buy
    :param symbol: the symbol of which you, want to buy.
    """

    current_price = fetch.fetch_symbol_currentprice(symbol)

    side = "buy" if action == "L" else "sell"
    # params = {'take_profit': take_profit, 'stop_loss': stop_loss} if action == 'L' else {
    #     'take_profit': stop_loss, 'stop_loss': take_profit}

    amount = trade_size / current_price
    execute.open_position(symbol, side, amount)


def invalidNonce_fix_somehow():
    print(EXCHANGE.load_time_difference())

    return


def liquidate(symbol: str):
    # does this completely close position?

    side = fetch.fetch_position_side(symbol)
    size = fetch.fetch_position_size(symbol)

    # generally will only be called if in position but in case
    # exit position here if not in position
    if side == "" or size == 0:
        return

    side = "sell" if (side == "long") else "buy"

    trade_res = execute.close_position(symbol=symbol, side=side, amount=size)

    return


def filter_trading_symbols(symbols: List[str], trade_size: int):
    """
    for now filters trading symbols on whether or not, size if big enough for
    minimum quantity
    *add more ways to filter as well as to turn on and off those you chose to use.
    *this was made from a mistake had enough money to buy but had
    to adjust in relation to precision.
    """
    markets = EXCHANGE.fetch_markets()
    final_list: list = []
    for i in markets:
        if i["id"] in symbols:
            if i["type"] == "spot":

                min_amount = float(i["info"]["minTradeQty"])
                amount_buy = trade_size / fetch.fetch_symbol_currentprice(i["id"])
                min_price_precision = float(i["info"]["minPricePrecision"])

                # nor more than min than dont ad
                if float(min_amount) > amount_buy:
                    continue
                if (min_price_precision) > amount_buy:
                    continue
                # add if survived min amount and min precision checks
                final_list.append(i["id"])
    print(final_list)
    return final_list


# split up into the ones used directly and the ones this file uses.
