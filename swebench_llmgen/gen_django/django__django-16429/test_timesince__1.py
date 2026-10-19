import datetime
import pytest
from django.utils.html import avoid_wrapping
from django.utils.timezone import is_aware
from django.utils.translation import gettext, ngettext_lazy

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
    now = datetime.datetime(2023, 10, 1, 12, 0, 0)

    # Test exact minute
    assert timesince(now - datetime.timedelta(minutes=1)) == "1 minute"
    assert timesince(now - datetime.timedelta(minutes=0)) == "0 minutes"

    # Test exact hour
    assert timesince(now - datetime.timedelta(hours=1)) == "1 hour"

    # Test multi-unit output
    assert timesince(now - datetime.timedelta(days=1, hours=2)) == "1 day, 2 hours"
    assert timesince(now - datetime.timedelta(days=15, hours=3, minutes=20)) == "2 weeks, 1 day"

    # Test future date
    assert timesince(now + datetime.timedelta(days=1)) == "0 minutes"
    
    # Test depth control
    assert timesince(now - datetime.timedelta(days=5, hours=3), depth=1) == "5 days"

    # Test with a custom time_strings dictionary
    custom_time_strings = {
        "year": "%(num)s year(s)",
        "month": "%(num)s month(s)",
        "week": "%(num)s week(s)",
        "day": "%(num)s day(s)",
        "hour": "%(num)s hour(s)",
        "minute": "%(num)s minute(s)",
    }
    
    assert timesince(now - datetime.timedelta(days=3, hours=12), time_strings=custom_time_strings) == "3 day(s), 12 hour(s)"
    
    # Test ValueError for depth <= 0
    with pytest.raises(ValueError):
        timesince(now, depth=0)

    # Test with aware datetime
    aware_now = now.astimezone(datetime.timezone.utc)
    assert timesince(aware_now - datetime.timedelta(hours=1), now=aware_now) == "1 hour"