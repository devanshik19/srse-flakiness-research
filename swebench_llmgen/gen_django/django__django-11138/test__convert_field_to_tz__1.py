import pytest
from django.conf import settings
from django.db.backends.oracle.operations import DatabaseOperations

@pytest.fixture
def db_operations():
    return DatabaseOperations()

def test_convert_field_to_tz_with_timezone(db_operations):
    settings.USE_TZ = True
    field_name = 'timestamp_field'
    tzname = 'America/New_York'
    expected_sql = "CAST((FROM_TZ(timestamp_field, '0:00') AT TIME ZONE 'America/New_York') AS TIMESTAMP)"
    result = db_operations._convert_field_to_tz(field_name, tzname)
    assert result == expected_sql

def test_convert_field_to_tz_without_timezone_setting(db_operations):
    settings.USE_TZ = False
    field_name = 'timestamp_field'
    tzname = 'America/New_York'
    result = db_operations._convert_field_to_tz(field_name, tzname)
    assert result == field_name

def test_convert_field_to_tz_with_invalid_timezone(db_operations):
    settings.USE_TZ = True
    field_name = 'timestamp_field'
    tzname = 'Invalid/Timezone'
    with pytest.raises(ValueError, match="Invalid time zone name: Invalid/Timezone"):
        db_operations._convert_field_to_tz(field_name, tzname)