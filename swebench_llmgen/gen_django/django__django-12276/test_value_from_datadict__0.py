import pytest
from django.forms.widgets import Widget

@pytest.mark.parametrize("data, name, expected", [
    ({"widget_name": "value"}, "widget_name", "value"),  # normal case
    ({}, "widget_name", None),                            # no data case
    ({"widget_name": None}, "widget_name", None),        # explicitly None case
    ({"other_name": "value"}, "widget_name", None),      # different name case
])
def test_value_from_datadict(data, name, expected):
    widget = Widget()
    result = widget.value_from_datadict(data, {}, name)
    assert result == expected