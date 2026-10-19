import pytest
from django.db.backends.base.operations import BaseDatabaseOperations

@pytest.mark.parametrize("input_value, expected_output", [
    ("192.168.1.1", "192.168.1.1"),
    (None, None),
    ("", None),
    ("::1", "::1"),
])
def test_adapt_ipaddressfield_value(input_value, expected_output):
    operations = BaseDatabaseOperations(None)
    result = operations.adapt_ipaddressfield_value(input_value)
    assert result == expected_output