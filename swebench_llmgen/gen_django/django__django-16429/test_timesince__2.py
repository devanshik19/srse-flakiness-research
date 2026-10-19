import datetime
import pytest
from django.utils.html import avoid_wrapping
from django.utils.timezone import is_aware
from django.utils.translation import gettext

# Assuming TIME_STRINGS, TIME_CHUNKS, and MONTHS_DAYS are defined similarly to the original source.
TIME_STRINGS = {
    "year": "%(num)s year" if 1 else "%(num)s years",
    "month": "%(num)s month" if 1 else "%(num)s months",
    "week": "%(num)s week" if 1 else "%(num)s weeks",
    "day": "%(num)s day" if 1 else "%(num)s days",
    "hour": "%(num)s hour" if 1 else "%(num)s hours",
    "minute": "%(num)s minute" if 1 else "%(num)s minutes",
}
TIME_CHUNKS = [60 * 60 * 24 * 30, 60 * 60 * 24, 60 * 60, 60]
MONTHS_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
TIME_STRINGS_KEYS = list(TIME_STRINGS.keys())

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
    now = datetime.datetime(2023, 10, 10, 12, 0, 0)

    # Test exact minute ago
    d1 = now - datetime.timedelta(minutes=1)
    assert timesince(d1, now) == "1 minute"

    # Test 2 minutes ago
    d2 = now - datetime.timedelta(minutes=2)
    assert timesince(d2, now) == "2 minutes"

    # Test 1 hour ago
    d3 = now - datetime.timedelta(hours=1)
    assert timesince(d3, now) == "1 hour"

    # Test 1 day ago
    d4 = now - datetime.timedelta(days=1)
    assert timesince(d4, now) == "1 day"

    # Test 1 month and 1 day ago
    d5 = now - datetime.timedelta(days=30 + 1)
    assert timesince(d5, now) == "1 month, 1 day"

    # Test 1 year ago
    d6 = now - datetime.timedelta(days=365)
    assert timesince(d6, now) == "1 year"

    # Test in the future (should return "0 minutes")
    d7 = now + datetime.timedelta(minutes=5)
    assert timesince(d7, now) == "0 minutes"

    # Test reversed
    assert timesince(now, d1, reversed=True) == "0 minutes"

    # Test ValueError for depth less than or equal to 0
    with pytest.raises(ValueError):
        timesince(now, depth=0)

    # Test when depth is set to 1
    assert timesince(d5, now, depth=1) == "1 month"

    # Test when depth is set greater than available parts
    assert timesince(d4, now, depth=3) == "1 day"