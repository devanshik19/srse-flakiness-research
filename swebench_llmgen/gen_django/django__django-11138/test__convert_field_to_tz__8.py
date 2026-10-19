import pytest
from django.conf import settings
from django.db.backends.oracle.operations import DatabaseOperations

# Set USE_TZ to True for testing
settings.USE_TZ = True

class TestDatabaseOperations:
    
    @pytest.fixture
    def db_operations(self):
        return DatabaseOperations()

    def test_convert_field_to_tz_valid_timezone(self, db_operations):
        field_name = 'created_at'
        tzname = 'UTC'
        result = db_operations._convert_field_to_tz(field_name, tzname)
        expected = "CAST((FROM_TZ(created_at, '0:00') AT TIME ZONE 'UTC') AS TIMESTAMP)"
        assert result == expected

    def test_convert_field_to_tz_invalid_timezone(self, db_operations):
        field_name = 'created_at'
        tzname = 'Invalid/Timezone'
        with pytest.raises(ValueError, match="Invalid time zone name: Invalid/Timezone"):
            db_operations._convert_field_to_tz(field_name, tzname)

    def test_convert_field_to_tz_no_tz(self, db_operations):
        settings.USE_TZ = False
        field_name = 'created_at'
        tzname = 'UTC'
        result = db_operations._convert_field_to_tz(field_name, tzname)
        assert result == field_name