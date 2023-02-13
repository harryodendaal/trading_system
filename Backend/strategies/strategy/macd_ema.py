from Backend.strategies.blocks.entering import (
    close_above_ema_and_macd_line_above_signal,
)
from Backend.strategies.blocks.managing.positions import macd_update_position


def before(self):
    return


def should_long(self):
    # return true if close is above EMA and MACD line is above signal line
    return close_above_ema_and_macd_line_above_signal(self.close, self.ema, self.macd)


def should_short(self):
    return False


def should_cancel(self):
    return True


def should_cancel_entry(self) -> bool:
    return True


def update_position(self):
    macd_update_position(self)
