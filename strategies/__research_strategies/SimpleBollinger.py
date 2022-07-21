"""
Simple Bollinger Bands Strategy
Timeframe: 1h
Repo: https://github.com/gabrielweich/jesse-strategies
When the price closes above the upperband in an uptrend (determined by the ichimoku cloud),
it gives a long signal indicating a possible continuation of the uptrend.
The position can also be closed when the price closes below lowerband, but the best results
were achieved when using the middleband instead.
"""


def filter_trend(self):
    # Only opens a long position when close is above ichimoku cloud
    return self.close > self.ichimoku.span_a and self.close > self.ichimoku.span_b


def filters(self):
    return [self.filter_trend]


def should_long(self) -> bool:
    # Go long if candle closes above upperband
    return self.close > self.bb[0]


def should_short(self) -> bool:
    return False


def should_cancel_entry(self) -> bool:
    return True


def should_cancel(self):
    return True


def update_position(self):
    # Close the position when candle closes below middleband
    if self.close < self.bb[1]:
        self.liquidate()


def before(self):
    return
