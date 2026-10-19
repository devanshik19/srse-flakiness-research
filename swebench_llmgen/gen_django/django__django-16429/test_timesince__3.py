import datetime
import pytest
from django.utils.html import avoid_wrapping
from django.utils.timezone import is_aware
from django.utils.translation import gettext, ngettext_lazy
from django.contrib.auth.models import User

TIME_STRINGS = {
    "year": "%(num)s year",
    "month": "%(num)s month",
    "week": "%(num)s week",
    "day": "%(num)s day",
    "hour": "%(num)s hour",
    "minute": "%(num)s minute",
}
TIME_STRINGS_KEYS = list(TIME_STRINGS.keys())
TIME_CHUNKS = [60 * 60 * 24 * 365, 60 * 60 * 24 * 30, 60 * 60 * 24 * 7, 60 * 60 * 24, 60 * 60, 60]
MONTHS_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def test_timesince_in_past():
    past_time = datetime.datetime.now() - datetime.timedelta(days=1, hours=2, minutes=30)
    result = timesince(past_time)
    assert "1 day" in result
    assert "2 hours" in result

def test_timesince_now():
    now = datetime.datetime.now()
    result = timesince(now)
    assert result == avoid_wrapping(TIME_STRINGS["minute"] % {"num": 0})

def test_timesince_in_future():
    future_time = datetime.datetime.now() + datetime.timedelta(days=1)
    result = timesince(future_time)
    assert result == avoid_wrapping(TIME_STRINGS["minute"] % {"num": 0})

def test_timesince_with_depth():
    past_time = datetime.datetime.now() - datetime.timedelta(days=365, hours=5, minutes=10)
    result = timesince(past_time, depth=2)
    assert "1 year" in result
    assert "5 hours" in result

def test_timesince_reversed():
    past_time = datetime.datetime.now() - datetime.timedelta(days=2)
    result = timesince(past_time, reversed=True)
    assert "0 minutes" in result

def test_timesince_custom_time_strings():
    custom_time_strings = {
        "year": "%(num)s years",
        "month": "%(num)s months",
        "week": "%(num)s weeks",
        "day": "%(num)s days",
        "hour": "%(num)s hours",
        "minute": "%(num)s minutes",
    }
    past_time = datetime.datetime.now() - datetime.timedelta(days=1)
    result = timesince(past_time, time_strings=custom_time_strings)
    assert "1 days" in result

def test_timesince_invalid_depth():
    with pytest.raises(ValueError):
        timesince(datetime.datetime.now(), depth=0)