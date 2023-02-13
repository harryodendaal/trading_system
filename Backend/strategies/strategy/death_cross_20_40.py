from Backend.strategies.blocks.entering import ema_cross
from Backend.strategies.blocks.managing.positions import dc_update_position

# overwrite strategy, then after finishing this part make it so that strategies are easy to test.


def before(self):
    return


def should_long(self):
    # 20 > 40 ; blue > red
    return ema_cross(self.short_ema, self.long_ema)


def should_short(self):
    return ema_cross(self.long_ema, self.short_ema)


def should_cancel_entry(self):
    return True


def update_position(self) -> None:
    dc_update_position(self)
