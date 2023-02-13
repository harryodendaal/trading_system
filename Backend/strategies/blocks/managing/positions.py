from Backend.exchange_interface.live_exchange_interface import liquidate


def dc_update_position(self):
    if self.is_long and self.short_ema < self.long_ema:
        liquidate(self.symbol)

    if self.is_short and self.short_ema > self.long_ema:
        liquidate(self.symbol)


def macd_update_position(self):
    # Close the position when MACD crosses below the signal line and closing prices is less than 100EMA

    if self.macd[0] < self.macd[1] and self.close < self.ema:
        self.liquidate("ETHUSDT")
