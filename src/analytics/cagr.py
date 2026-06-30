import math


def calculate_cagr(start_value, end_value, years):
    """
    Calculates CAGR.

    Returns:
    (value, flag)
    """

    if years <= 0:
        return None, "INVALID_PERIOD"

    if start_value == 0:
        return None, "ZERO_BASE"

    if years < 3:
        return None, "INSUFFICIENT"

    if start_value > 0 and end_value > 0:

        cagr = (
            (end_value / start_value) ** (1 / years) - 1
        ) * 100

        return round(cagr, 2), "NORMAL"

    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    return None, "UNKNOWN"