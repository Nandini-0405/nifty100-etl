import pytest

from src.analytics.ratios import *


def test_net_profit_margin():

    assert net_profit_margin(20,100)==20


def test_npm_zero_sales():

    assert net_profit_margin(10,0) is None


def test_operating_profit_margin():

    assert operating_profit_margin(30,100)==30


def test_opm_check():

    assert check_opm(25,23)==True


def test_roe():

    assert round(
        return_on_equity(20,50,50),
        2
    )==20


def test_negative_equity():

    assert return_on_equity(
        20,
        -50,
        -60
    ) is None


def test_roce():

    value = return_on_capital_employed(
        20,
        5,
        50,
        50,
        50
    )

    assert round(value,2)==16.67


def test_roa():

    assert round(
        return_on_assets(
            20,
            100
        ),
        2
    )==20
    