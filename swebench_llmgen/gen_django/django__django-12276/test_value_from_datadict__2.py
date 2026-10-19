import pytest
from django.forms.widgets import Widget

@pytest.mark.parametrize("data, name, expected", [
    ({"field": "value"}, "field", "value"),  # Test basic retrieval
    ({"field": ""}, "field", ""),            # Test empty string retrieval
    ({"field": None}, "field", None),        # Test None retrieval
    ({}, "field", None),                     # Test no data provided
])
def test_value_from_datadict(data, name, expected):
    widget = Widget()
    result = widget.value_from_datadict(data, None, name)
    assert result == expected