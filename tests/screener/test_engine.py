from src.screener.engine import ScreenerEngine


def test_quality_compounder():

    engine = ScreenerEngine()

    df = engine.apply_filters(
        "quality_compounder"
    )

    assert len(df) > 0

    engine.close()


def test_value_pick():

    engine = ScreenerEngine()

    df = engine.apply_filters(
        "value_pick"
    )

    assert len(df) > 0

    engine.close()