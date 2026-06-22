from src.etl.validator import log_failure

def test_validator_exists():
    assert log_failure is not None