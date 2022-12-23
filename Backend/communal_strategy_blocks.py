import numpy as np


def trend_from_pivot_points(candles: np.ndarray, type: str):
    # Important possible changes:
    # must close below the wick?
    # should also test a bit more. might also expand it a bit more: " not break the retraction level of the impulse."
    # https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/pivot-points-high-low

    # OPTIMISATION:
    # if there are not 5 consecutive ones, we dont have to assess.
    # a way for this info to persist and not have to be recalculated? THIS IS Important.

    pp_length = 10
    candles = np.flip(candles, 0)
    pivot_highs = {}
    pivot_lows = {}

    for idx in range(1+pp_length, len(candles)):
        if (idx > len(candles) - (pp_length+1)):
            break

        # search for pivot highs
        # the current candle is bigger than 10 to it's left
        if (candles[idx][3] >= max(candles[idx: idx + (pp_length+1)][:, 3])):
            # the current candle is bigger than 10 to it's right.
            if (candles[idx][3] >= max(candles[idx - (pp_length + 1): idx][:, 3])):
                # store both idx and value.
                pivot_highs[idx] = candles[idx][3]

        # search for pivot lows
        if (candles[idx][3] <= min(candles[idx: idx + (pp_length+1)][:, 3])):
            if (candles[idx][3] <= min(candles[idx - (pp_length + 1): idx][:, 3])):
                pivot_lows[idx] = candles[idx][3]

        if (len(pivot_highs) > 2 and len(pivot_lows) > 2):
            break

    pivot_low_keys = (list(pivot_lows.keys()))
    pivot_high_keys = (list(pivot_highs.keys()))

    # Uptrend: previous low is not lower and previous high is higher
    if (type == 'u'):
        if (pivot_lows[pivot_low_keys[0]] > pivot_lows[pivot_low_keys[1]]):
            if (pivot_highs[pivot_high_keys[0]] > pivot_highs[pivot_high_keys[1]]):
                return True

    # Downtrend:
    if (type == 'd'):
        if (pivot_lows[pivot_low_keys[0]] < pivot_lows[pivot_low_keys[1]]):
            if (pivot_highs[pivot_high_keys[0]] < pivot_highs[pivot_high_keys[1]]):
                return True
    return False
