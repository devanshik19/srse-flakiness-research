import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.db.backends.oracle.operations import DatabaseOperations

# Set up a simple regex for timezone matching as it is not defined in the provided source.
DatabaseOperations._tzname_re = re.compile(r'^[A-Za-z/_]+$')

def test_convert_field_to_tz_valid():
    # Arrange
    ops = DatabaseOperations()
    field_name = 'timestamp_field'
    tzname = 'UTC'

    # Act
    result = ops._convert_field_to_tz(field_name, tzname)

    # Assert
    expected_result = "CAST((FROM_TZ(%s, '0:00') AT TIME ZONE '%s') AS TIMESTAMP)" % (field_name, tzname)
    assert result == expected_result

def test_convert_field_to_tz_invalid_timezone():
    # Arrange
    ops = DatabaseOperations()
    field_name = 'timestamp_field'
    invalid_tzname = 'INVALID_TZ'

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid time zone name: %s" % invalid_tzname):
        ops._convert_field_to_tz(field_name, invalid_tzname)

def test_convert_field_to_tz_with_timezone_support_disabled():
    # Arrange
    ops = DatabaseOperations()
    field_name = 'timestamp_field'
    valid_tzname = 'UTC'
    
    # Disable timezone support
    original_use_tz = settings.USE_TZ
    settings.USE_TZ = False

    # Act
    result = ops._convert_field_to_tz(field_name, valid_tzname)

    # Assert
    assert result == field_name

    # Restore settings
    settings.USE_TZ = original_use_tz