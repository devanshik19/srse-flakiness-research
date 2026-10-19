import datetime
from django.utils.html import avoid_wrapping
from django.utils.timezone import is_aware
from django.utils.translation import gettext, ngettext_lazy
from django.contrib.auth.models import User
from django.utils.timesince import timesince

def test_timesince():
    # Test case 1: Past datetime
    past_date = datetime.datetime(2021, 1, 1, 12, 0, 0)
    result = timesince(past_date)
    assert "minutes" in result or "hours" in result or "days" in result

    # Test case 2: Future datetime (should return "0 minutes")
    future_date = datetime.datetime(3000, 1, 1, 12, 0, 0)
    result = timesince(future_date)
    assert result == avoid_wrapping("0 minutes")

    # Test case 3: Current datetime
    now = datetime.datetime.now()
    result = timesince(now)
    assert result == avoid_wrapping("0 minutes")

    # Test case 4: Specific reversed case
    result = timesince(past_date, now=now, reversed=True)
    assert result == avoid_wrapping("0 minutes")

    # Test case 5: Testing for depth
    result = timesince(past_date, depth=2)
    assert isinstance(result, str)

    # Test case 6: Invalid depth parameter
    import pytest
    with pytest.raises(ValueError, match="depth must be greater than 0."):
        timesince(past_date, depth=0)

    # Test case 7: Using time_strings
    custom_time_strings = {
        "year": "%(num)d year",
        "month": "%(num)d month",
        "week": "%(num)d week",
        "day": "%(num)d day",
        "hour": "%(num)d hour",
        "minute": "%(num)d minute",
    }
    result = timesince(past_date, time_strings=custom_time_strings)
    assert any(unit in result for unit in ["year", "month", "week", "day", "hour", "minute"])