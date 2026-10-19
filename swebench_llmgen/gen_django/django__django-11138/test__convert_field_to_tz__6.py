import pytest
from django.conf import settings
from django.db.backends.oracle.operations import DatabaseOperations

@pytest.fixture
def db_operations():
    return DatabaseOperations()

def test_convert_field_to_tz_without_tz():
    settings.USE_TZ = False
    db_ops = DatabaseOperations()
    result = db_ops._convert_field_to_tz('my_field', 'UTC')
    assert result == 'my_field'

def test_convert_field_to_tz_with_valid_tz():
    settings.USE_TZ = True
    db_ops = DatabaseOperations()
    result = db_ops._convert_field_to_tz('my_field', 'UTC')
    expected_result = "CAST((FROM_TZ(my_field, '0:00') AT TIME ZONE 'UTC') AS TIMESTAMP)"
    assert result == expected_result

def test_convert_field_to_tz_with_invalid_tz():
    settings.USE_TZ = True
    db_ops = DatabaseOperations()
    with pytest.raises(ValueError, match="Invalid time zone name: Invalid/Timezone"):
        db_ops._convert_field_to_tz('my_field', 'Invalid/Timezone')