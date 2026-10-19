import pytest
import datetime
from django.utils.html import avoid_wrapping
from django.utils.timezone import is_aware
from django.utils.translation import gettext, ngettext_lazy
from django.contrib.auth.models import User

TIME_STRINGS = {
    "year": "%(num)d year",
    "month": "%(num)d month",
    "week": "%(num)d week",
    "day": "%(num)d day",
    "hour": "%(num)d hour",
    "minute": "%(num)d minute",
}
TIME_STRINGS_KEYS = list(TIME_STRINGS.keys())
TIME_CHUNKS = [365 * 24 * 60 * 60, 30 * 24 * 60 * 60, 7 * 24 * 60 * 60, 24 * 60 * 60, 60 * 60, 60]
MONTHS_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def timesince(d, now=None, reversed=False, time_strings=None, depth=2):
    # Implementation of the timesince function as provided

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
    now = datetime.datetime.now(datetime.timezone.utc)
    past_datetime = now - datetime.timedelta(days=1, hours=2, minutes=3)
    future_datetime = now + datetime.timedelta(days=1)

    # Test normal case
    assert timesince(past_datetime) == "1 day, 2 hours"

    # Test reversed
    assert timesince(past_datetime, reversed=True) == "0 minutes"

    # Test with depth
    assert timesince(past_datetime, depth=3) == "1 day, 2 hours"

    # Test future date
    assert timesince(future_datetime) == "0 minutes"

    # Test edge case (same time)
    assert timesince(now) == "0 minutes"

    # Test with time_strings
    custom_strings = {
        "year": "%(num)d year",
        "month": "%(num)d month",
        "week": "%(num)d week",
        "day": "%(num)d day",
        "hour": "%(num)d hour",
        "minute": "%(num)d minute",
    }
    assert timesince(past_datetime, time_strings=custom_strings) == "1 day, 2 hours"

    # Test negative depth
    with pytest.raises(ValueError):
        timesince(past_datetime, depth=0)

    # Test invalid datetime input
    assert timesince(datetime.date.today()) == "0 minutes"