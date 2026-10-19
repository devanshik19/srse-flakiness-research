import datetime
import re
import uuid
from functools import lru_cache
from django.conf import settings
from django.db.backends.base.operations import BaseDatabaseOperations
from django.db.backends.utils import strip_quotes, truncate_name
from django.db.utils import DatabaseError
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.functional import cached_property
from django.contrib.auth.models import User
import pytest

class TestDatabaseOperations:
    
    @pytest.fixture
    def db_operations(self):
        return DatabaseOperations()

    def test_convert_field_to_tz_without_timezone(self, db_operations):
        settings.USE_TZ = False
        result = db_operations._convert_field_to_tz("my_field", "UTC")
        assert result == "my_field"

    def test_convert_field_to_tz_with_valid_timezone(self, db_operations):
        settings.USE_TZ = True
        db_operations._tzname_re = re.compile(r'^[A-Za-z/_]+$')
        result = db_operations._convert_field_to_tz("my_field", "UTC")
        expected = "CAST((FROM_TZ(my_field, '0:00') AT TIME ZONE 'UTC') AS TIMESTAMP)"
        assert result == expected

    def test_convert_field_to_tz_with_invalid_timezone(self, db_operations):
        settings.USE_TZ = True
        db_operations._tzname_re = re.compile(r'^[A-Za-z/_]+$')
        with pytest.raises(ValueError, match="Invalid time zone name"):
            db_operations._convert_field_to_tz("my_field", "Invalid/Timezone")