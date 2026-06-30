from src.analytics.ratios import *

# ==========================
# Day 08 Tests
# ==========================

def test_net_profit_margin():
    assert net_profit_margin(20, 100) == 20


def test_npm_zero_sales():
    assert net_profit_margin(10, 0) is None


def test_operating_profit_margin():
    assert operating_profit_margin(30, 100) == 30


def test_opm_check():
    assert check_opm(25, 23) is True


def test_roe():
    assert round(return_on_equity(20, 50, 50), 2) == 20


def test_negative_equity():
    assert return_on_equity(20, -50, -60) is None


def test_roce():
    value = return_on_capital_employed(
        20,
        5,
        50,
        50,
        50
    )

    assert round(value, 2) == 16.67


def test_roa():
    assert round(return_on_assets(20, 100), 2) == 20


# ==========================
# Day 09 Tests
# ==========================

def test_debt_to_equity():
    assert debt_to_equity(50, 50, 50) == 0.5


def test_debt_free():
    assert debt_to_equity(0, 50, 50) == 0


def test_interest_coverage():
    assert interest_coverage(100, 20, 10) == 12


def test_interest_zero():
    assert interest_coverage(100, 20, 0) is None


def test_icr_label():
    assert icr_label(None) == "Debt Free"


def test_high_leverage():
    assert high_leverage_flag(6, "IT") is True


def test_net_debt():
    assert net_debt(100, 40) == 60


def test_asset_turnover():
    assert asset_turnover(200, 100) == 2