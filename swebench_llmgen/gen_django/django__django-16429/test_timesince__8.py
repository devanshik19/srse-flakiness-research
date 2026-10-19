import datetime
import pytest
from django.utils.html import avoid_wrapping
from django.utils.timezone import is_aware
from django.utils.translation import gettext

# Assuming TIME_STRINGS and other constants are defined as needed
TIME_STRINGS = {
    "year": "%(num)d year",
    "month": "%(num)d month",
    "week": "%(num)d week",
    "day": "%(num)d day",
    "hour": "%(num)d hour",
    "minute": "%(num)d minute",
}
TIME_STRINGS_KEYS = list(TIME_STRINGS.keys())
TIME_CHUNKS = [60 * 60 * 24 * 7, 60 * 60 * 24, 60 * 60, 60]

def test_timesince():
    now = datetime.datetime(2023, 10, 10, 12, 0, 0, tzinfo=datetime.timezone.utc)

    # Test case 1: Normal case
    past_date = datetime.datetime(2023, 10, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
    result = timesince(past_date, now)
    assert result == avoid_wrapping("9 days")

    # Test case 2: No time difference
    past_date = datetime.datetime(2023, 10, 10, 12, 0, 0, tzinfo=datetime.timezone.utc)
    result = timesince(past_date, now)
    assert result == avoid_wrapping("0 minutes")

    # Test case 3: Future date
    future_date = datetime.datetime(2023, 10, 15, 12, 0, 0, tzinfo=datetime.timezone.utc)
    result = timesince(future_date, now)
    assert result == avoid_wrapping("0 minutes")

    # Test case 4: Custom depth
    past_date = datetime.datetime(2022, 10, 10, 0, 0, 0, tzinfo=datetime.timezone.utc)
    result = timesince(past_date, now, depth=1)
    assert result == avoid_wrapping("0 years")

    # Test case 5: Reverse parameter
    past_date = datetime.datetime(2023, 10, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
    result = timesince(past_date, now, reversed=True)
    assert result == avoid_wrapping("9 days")

    # Test case 6: Invalid depth
    with pytest.raises(ValueError, match="depth must be greater than 0."):
        timesince(past_date, now, depth=0)

    # Test case 7: Using time_strings argument
    custom_time_strings = {
        "year": "%(num)d yr",
        "month": "%(num)d mo",
        "week": "%(num)d wk",
        "day": "%(num)d d",
        "hour": "%(num)d h",
        "minute": "%(num)d min",
    }
    result = timesince(past_date, now, time_strings=custom_time_strings)
    assert result == avoid_wrapping("9 days")