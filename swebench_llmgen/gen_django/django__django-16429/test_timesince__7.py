import pytest
import datetime
from django.utils.html import avoid_wrapping
from django.utils.timezone import is_aware
from django.utils.translation import gettext

# Constants for time strings and time chunks
TIME_STRINGS = {
    "year": "%(num)d year",
    "month": "%(num)d month",
    "week": "%(num)d week",
    "day": "%(num)d day",
    "hour": "%(num)d hour",
    "minute": "%(num)d minute",
}
TIME_STRINGS_KEYS = ["year", "month", "week", "day", "hour", "minute"]
TIME_CHUNKS = [31536000, 2592000, 604800, 86400, 3600, 60]
MONTHS_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def timesince(d, now=None, reversed=False, time_strings=None, depth=2):
    if time_strings is None:
        time_strings = TIME_STRINGS
    if depth <= 0:
        raise ValueError("depth must be greater than 0.")
    
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year, d.month, d.day)
    if now and not isinstance(now, datetime.datetime):
        now = datetime.datetime(now.year, now.month, now.day)

    now = now or datetime.datetime.now(datetime.timezone.utc if is_aware(d) else None)

    if reversed:
        d, now = now, d
    delta = now - d

    since = delta.days * 24 * 60 * 60 + delta.seconds
    if since <= 0:
        return avoid_wrapping(time_strings["minute"] % {"num": 0})

    total_months = (now.year - d.year) * 12 + (now.month - d.month)
    if d.day > now.day or (d.day == now.day and d.time() > now.time()):
        total_months -= 1
    years, months = divmod(total_months, 12)

    if years or months:
        pivot_year = d.year + years
        pivot_month = d.month + months
        if pivot_month > 12:
            pivot_month -= 12
            pivot_year += 1
        pivot = datetime.datetime(
            pivot_year,
            pivot_month,
            min(MONTHS_DAYS[pivot_month - 1], d.day),
            d.hour,
            d.minute,
            d.second,
        )
    else:
        pivot = d
    remaining_time = (now - pivot).total_seconds()
    partials = [years, months]
    for chunk in TIME_CHUNKS:
        count = remaining_time // chunk
        partials.append(count)
        remaining_time -= chunk * count

    i = 0
    for i, value in enumerate(partials):
        if value != 0:
            break
    else:
        return avoid_wrapping(time_strings["minute"] % {"num": 0})

    result = []
    current_depth = 0
    while i < len(TIME_STRINGS_KEYS) and current_depth < depth:
        value = partials[i]
        if value == 0:
            break
        name = TIME_STRINGS_KEYS[i]
        result.append(avoid_wrapping(time_strings[name] % {"num": value}))
        current_depth += 1
        i += 1

    return gettext(", ").join(result)

def test_timesince():
    # Test for the current time
    now = datetime.datetime.now(datetime.timezone.utc)
    assert timesince(now) == avoid_wrapping(TIME_STRINGS["minute"] % {"num": 0})

    # Test for 10 minutes ago
    ten_minutes_ago = now - datetime.timedelta(minutes=10)
    assert timesince(ten_minutes_ago) == avoid_wrapping(TIME_STRINGS["minute"] % {"num": 10})

    # Test for 1 hour ago
    one_hour_ago = now - datetime.timedelta(hours=1)
    assert timesince(one_hour_ago) == avoid_wrapping(TIME_STRINGS["hour"] % {"num": 1})

    # Test for 2 hours and 15 minutes ago
    two_hours_15_minutes_ago = now - datetime.timedelta(hours=2, minutes=15)
    assert timesince(two_hours_15_minutes_ago) == avoid_wrapping(TIME_STRINGS["hour"] % {"num": 2}) + ", " + avoid_wrapping(TIME_STRINGS["minute"] % {"num": 15})

    # Test for 30 days ago
    thirty_days_ago = now - datetime.timedelta(days=30)
    assert timesince(thirty_days_ago) == avoid_wrapping(TIME_STRINGS["month"] % {"num": 1}) + ", " + avoid_wrapping(TIME_STRINGS["day"] % {"num": 0})

    # Test for depth parameter
    assert timesince(now - datetime.timedelta(days=400), depth=3) == avoid_wrapping(TIME_STRINGS["year"] % {"num": 1}) + ", " + avoid_wrapping(TIME_STRINGS["month"] % {"num": 1})

    # Test for future time
    future_time = now + datetime.timedelta(minutes=5)
    assert timesince(future_time) == avoid_wrapping(TIME_STRINGS["minute"] % {"num": 0})

    # Test for reversed
    assert timesince(now, now - datetime.timedelta(minutes=10), reversed=True) == avoid_wrapping(TIME_STRINGS["minute"] % {"num": 10})

    # Test invalid depth
    with pytest.raises(ValueError):
        timesince(now, depth=0)