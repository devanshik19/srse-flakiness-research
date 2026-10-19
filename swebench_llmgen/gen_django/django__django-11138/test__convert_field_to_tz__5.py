import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.db.backends.oracle.operations import DatabaseOperations


class TestDatabaseOperations:
    
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.operations = DatabaseOperations()
        self.operations._tzname_re = re.compile(r'^[\w+/]+(?:/[\w.]+)?$')
    
    def test_convert_field_to_tz_with_use_tz_on(self):
        settings.USE_TZ = True
        field_name = 'last_login'
        tzname = 'UTC'
        
        result = self.operations._convert_field_to_tz(field_name, tzname)
        
        expected_result = "CAST((FROM_TZ(%s, '0:00') AT TIME ZONE '%s') AS TIMESTAMP)" % (field_name, tzname)
        assert result == expected_result

    def test_convert_field_to_tz_raises_value_error_for_invalid_tzname(self):
        settings.USE_TZ = True
        field_name = 'last_login'
        invalid_tzname = 'Invalid/Timezone'
        
        with pytest.raises(ValueError, match="Invalid time zone name: %s" % invalid_tzname):
            self.operations._convert_field_to_tz(field_name, invalid_tzname)

    def test_convert_field_to_tz_returns_field_name_when_use_tz_off(self):
        settings.USE_TZ = False
        field_name = 'last_login'
        tzname = 'UTC'
        
        result = self.operations._convert_field_to_tz(field_name, tzname)
        
        assert result == field_name