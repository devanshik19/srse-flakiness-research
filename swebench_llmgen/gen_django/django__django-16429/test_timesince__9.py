import pytest
import datetime
from django.utils.html import avoid_wrapping
from django.utils.timezone import is_aware
from django.utils.translation import gettext, ngettext_lazy
from django.utils.timesince import timesince

TIME_STRINGS = {
    "year": "%(num)s year",
    "month": "%(num)s month",
    "week": "%(num)s week",
    "day": "%(num)s day",
    "hour": "%(num)s hour",
    "minute": "%(num)s minute",
}
TIME_STRINGS_KEYS = ["year", "month", "week", "day", "hour", "minute"]
TIME_CHUNKS = [365 * 24 * 60 * 60, 30 * 24 * 60 * 60, 7 * 24 * 60 * 60, 24 * 60 * 60, 60 * 60, 60]
MONTHS_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def test_timesince_with_past_date():
    past_date = datetime.datetime(2022, 1, 1, 12, 0, 0)
    result = timesince(past_date)
    assert "year" in result or "month" in result or "day" in result or "hour" in result or "minute" in result

def test_timesince_with_now():
    now = datetime.datetime.now()
    result = timesince(now)
    assert result == avoid_wrapping(TIME_STRINGS["minute"] % {"num": 0})

def test_timesince_with_future_date():
    future_date = datetime.datetime(2023, 1, 1, 12, 0, 0)
    result = timesince(future_date)
    assert result == avoid_wrapping(TIME_STRINGS["minute"] % {"num": 0})

def test_timesince_with_depth():
    past_date = datetime.datetime(2020, 1, 1, 12, 0, 0)
    result = timesince(past_date, depth=2)
    assert sum(k in result for k in ["year", "month", "week", "day", "hour", "minute"]) <= 2

def test_timesince_with_custom_time_strings():
    custom_time_strings = {
        "year": "Yr %(num)s",
        "month": "Mo %(num)s",
        "week": "Wk %(num)s",
        "day": "D %(num)s",
        "hour": "Hr %(num)s",
        "minute": "Min %(num)s",
    }
    past_date = datetime.datetime(2021, 1, 1, 12, 0, 0)
    result = timesince(past_date, time_strings=custom_time_strings)
    assert "Yr" in result or "Mo" in result or "D" in result or "Hr" in result or "Min" in result

def test_timesince_invalid_depth():
    with pytest.raises(ValueError):
        timesince(datetime.datetime.now(), depth=0)