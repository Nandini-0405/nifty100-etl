from src.analytics.cashflow_kpis import *


def test_free_cash_flow():

    assert free_cash_flow(100,-40)==60


def test_cfo_quality():

    assert cfo_quality_score(120,100)=="High Quality"


def test_cfo_quality_none():

    assert cfo_quality_score(10,0) is None


def test_capex():

    value,label=capex_intensity(-20,500)

    assert label=="Moderate"


def test_capex_asset_light():

    value,label=capex_intensity(-5,500)

    assert label=="Asset Light"


def test_fcf_conversion():

    assert fcf_conversion_rate(50,100)==50


def test_fcf_none():

    assert fcf_conversion_rate(50,0) is None


def test_pattern():

    assert capital_allocation_pattern(
        100,
        -50,
        -30
    )=="Reinvestor"