import pytest
from django.conf import settings
from django.db.backends.oracle.operations import DatabaseOperations

@pytest.mark.parametrize("use_tz, tzname, expected", [
    (True, 'UTC', "CAST((FROM_TZ(field_name, '0:00') AT TIME ZONE 'UTC') AS TIMESTAMP)"),
    (True, 'America/New_York', "CAST((FROM_TZ(field_name, '0:00') AT TIME ZONE 'America/New_York') AS TIMESTAMP)"),
    (False, 'UTC', "field_name"),
])
def test_convert_field_to_tz(monkeypatch, use_tz, tzname, expected):
    monkeypatch.setattr(settings, 'USE_TZ', use_tz)

    ops = DatabaseOperations()
    ops._tzname_re = re.compile(r"^[\w\/]+$")  # Simple regex to match timezone names.

    if not use_tz or tzname == 'UTC':
        result = ops._convert_field_to_tz("field_name", tzname)
        assert result == expected
    else:
        # Use pytest.raises for invalid timezone name
        if tzname == 'Invalid/Timezone':
            with pytest.raises(ValueError, match="Invalid time zone name"):
                ops._convert_field_to_tz("field_name", tzname)
        else:
            result = ops._convert_field_to_tz("field_name", tzname)
            assert result == expected