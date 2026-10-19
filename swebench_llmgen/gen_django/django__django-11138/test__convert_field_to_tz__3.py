import pytest
from django.conf import settings
from django.db.backends.oracle.operations import DatabaseOperations

@pytest.fixture
def db_operations():
    return DatabaseOperations()

def test_convert_field_to_tz_with_utc_disabled(db_operations):
    settings.USE_TZ = False
    field_name = 'my_field'
    result = db_operations._convert_field_to_tz(field_name, 'UTC')
    assert result == field_name

def test_convert_field_to_tz_with_valid_timezone(db_operations):
    settings.USE_TZ = True
    db_operations._tzname_re = re.compile(r'^[\w\-/]+$')  # simple valid TZ pattern
    field_name = 'my_field'
    tzname = 'America/New_York'
    result = db_operations._convert_field_to_tz(field_name, tzname)
    expected = f"CAST((FROM_TZ(my_field, '0:00') AT TIME ZONE 'America/New_York') AS TIMESTAMP)"
    assert result == expected

def test_convert_field_to_tz_with_invalid_timezone(db_operations):
    settings.USE_TZ = True
    db_operations._tzname_re = re.compile(r'^[\w\-/]+$')
    field_name = 'my_field'
    tzname = 'Invalid/Timezone'
    with pytest.raises(ValueError, match=f"Invalid time zone name: {tzname}"):
        db_operations._convert_field_to_tz(field_name, tzname)