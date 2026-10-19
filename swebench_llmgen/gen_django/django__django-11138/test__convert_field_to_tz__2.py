import pytest
import re
from django.conf import settings
from django.db.backends.oracle.operations import DatabaseOperations

@pytest.mark.parametrize("use_tz, tzname, expected", [
    (True, 'UTC', "CAST((FROM_TZ(%s, '0:00') AT TIME ZONE 'UTC') AS TIMESTAMP)"),
    (True, 'America/New_York', "CAST((FROM_TZ(%s, '0:00') AT TIME ZONE 'America/New_York') AS TIMESTAMP)"),
    (False, 'UTC', "%s"),
    (False, 'America/New_York', "%s"),
])
def test_convert_field_to_tz(settings, use_tz, tzname, expected):
    settings.USE_TZ = use_tz
    db_ops = DatabaseOperations()
    db_ops._tzname_re = re.compile(r'^[a-zA-Z/_]+$')

    field_name = 'some_field'
    result = db_ops._convert_field_to_tz(field_name, tzname)

    assert result == expected % field_name

def test_convert_field_to_tz_invalid_timezone(settings):
    settings.USE_TZ = True
    db_ops = DatabaseOperations()
    db_ops._tzname_re = re.compile(r'^[a-zA-Z/_]+$')

    with pytest.raises(ValueError, match="Invalid time zone name: Invalid/Timezone"):
        db_ops._convert_field_to_tz('some_field', 'Invalid/Timezone')