def ema_cross(above, below):
    return above > below


def close_above_ema_and_macd_line_above_signal(close, ema, macd):
    return close > ema and macd[0] > macd[1]


# def
