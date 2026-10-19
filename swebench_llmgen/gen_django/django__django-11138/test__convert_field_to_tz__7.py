import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.db import connections
from django.db.backends.oracle.operations import DatabaseOperations

@pytest.fixture
def db_operations():
    return DatabaseOperations()

def test_convert_field_to_tz_with_timezone(db_operations):
    settings.USE_TZ = True
    db_operations._tzname_re = re.compile(r'^[A-Za-z/_]+$')
    field_name = "timestamp_field"
    tzname = "America/New_York"
    expected_sql = "CAST((FROM_TZ(%s, '0:00') AT TIME ZONE '%s') AS TIMESTAMP)" % (field_name, tzname)
    
    result = db_operations._convert_field_to_tz(field_name, tzname)
    
    assert result == expected_sql

def test_convert_field_to_tz_without_timezone(db_operations):
    settings.USE_TZ = False
    field_name = "timestamp_field"
    tzname = "America/New_York"
    
    result = db_operations._convert_field_to_tz(field_name, tzname)
    
    assert result == field_name

def test_convert_field_to_tz_invalid_timezone(db_operations):
    settings.USE_TZ = True
    db_operations._tzname_re = re.compile(r'^[A-Za-z/_]+$')
    field_name = "timestamp_field"
    
    with pytest.raises(ValueError, match="Invalid time zone name: invalid_tz"):
        db_operations._convert_field_to_tz(field_name, "invalid_tz")