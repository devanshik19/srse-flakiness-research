import pytest
import datetime
from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _

# Test dataset for various edge cases
test_cases = [
    # (input datetime, now datetime, expected output string, depth, reversed)
    (datetime.datetime(2023, 10, 15, 12, 0, 0, tzinfo=datetime.timezone.utc),
     datetime.datetime(2023, 10, 15, 12, 10, 0, tzinfo=datetime.timezone.utc),
     _("10 minutes"), 2, False),
    
    (datetime.datetime(2023, 10, 15, 12, 0, 0, tzinfo=datetime.timezone.utc),
     None,
     _("0 minutes"), 2, False),
    
    (datetime.datetime(2023, 10, 15, 12, 0, 0, tzinfo=datetime.timezone.utc),
     datetime.datetime(2023, 10, 15, 12, 0, 10, tzinfo=datetime.timezone.utc),
     _("0 minutes"), 2, False),
    
    (datetime.datetime(2023, 10, 15, 11, 30, 0, tzinfo=datetime.timezone.utc),
     datetime.datetime(2023, 10, 15, 12, 0, 0, tzinfo=datetime.timezone.utc),
     _("30 minutes"), 2, False),
    
    (datetime.datetime(2023, 9, 15, 12, 0, 0, tzinfo=datetime.timezone.utc),
     datetime.datetime(2023, 10, 15, 12, 0, 0, tzinfo=datetime.timezone.utc),
     _("1 month"), 2, False),
    
    (datetime.datetime(2022, 10, 15, 12, 0, 0, tzinfo=datetime.timezone.utc),
     datetime.datetime(2023, 10, 15, 12, 0, 0, tzinfo=datetime.timezone.utc),
     _("1 year"), 2, False),
    
    (datetime.datetime(2023, 10, 1, 12, 0, 0, tzinfo=datetime.timezone.utc),
     datetime.datetime(2023, 10, 15, 12, 0, 0, tzinfo=datetime.timezone.utc),
     _("2 weeks"), 2, False),
]

@pytest.mark.parametrize("d, now, expected, depth, reversed", test_cases)
def test_timesince(d, now, expected, depth, reversed):
    result = timesince(d, now, depth=depth, reversed=reversed)
    assert result == expected

def test_timesince_invalid_depth():
    with pytest.raises(ValueError, match="depth must be greater than 0."):
        timesince(datetime.datetime.now(), depth=0)