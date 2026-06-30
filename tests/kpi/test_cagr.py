from src.analytics.cagr import calculate_cagr
def test_normal_cagr():

    value, flag = calculate_cagr(
        100,
        150,
        5
    )

    assert flag == "NORMAL"


def test_zero_base():

    value, flag = calculate_cagr(
        0,
        100,
        5
    )

    assert flag == "ZERO_BASE"


def test_turnaround():

    value, flag = calculate_cagr(
        -100,
        100,
        5
    )

    assert flag == "TURNAROUND"


def test_decline_to_loss():

    value, flag = calculate_cagr(
        100,
        -100,
        5
    )

    assert flag == "DECLINE_TO_LOSS"


def test_both_negative():

    value, flag = calculate_cagr(
        -100,
        -50,
        5
    )

    assert flag == "BOTH_NEGATIVE"


def test_insufficient_years():

    value, flag = calculate_cagr(
        100,
        150,
        2
    )

    assert flag == "INSUFFICIENT"


def test_invalid_period():

    value, flag = calculate_cagr(
        100,
        150,
        0
    )

    assert flag == "INVALID_PERIOD"


def test_positive_growth():

    value, flag = calculate_cagr(
        200,
        400,
        5
    )

    assert value > 0


def test_negative_growth():

    value, flag = calculate_cagr(
        400,
        200,
        5
    )

    assert value < 0


def test_return_type():

    value, flag = calculate_cagr(
        100,
        200,
        5
    )

    assert isinstance(flag, str)