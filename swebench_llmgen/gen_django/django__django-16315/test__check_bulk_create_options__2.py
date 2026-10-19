import pytest
from django.contrib.auth.models import User
from django.db import connections, NotSupportedError
from django.db.models.query import QuerySet
from django.core.exceptions import ValidationError

@pytest.mark.parametrize("ignore_conflicts, update_conflicts, update_fields, unique_fields, expected", [
    (True, False, None, None, "IGNORE"),
    (False, True, ['username'], ['email'], "UPDATE"),
    (False, False, None, None, None),
])
def test_check_bulk_create_options_valid_cases(ignore_conflicts, update_conflicts, update_fields, unique_fields, expected):
    qs = QuerySet(model=User)

    if expected == "IGNORE":
        result = qs._check_bulk_create_options(ignore_conflicts=True, update_conflicts=False, update_fields=None, unique_fields=None)
        assert result == expected
    elif expected == "UPDATE":
        result = qs._check_bulk_create_options(ignore_conflicts=False, update_conflicts=True, update_fields=update_fields, unique_fields=unique_fields)
        assert result == expected
    else:
        result = qs._check_bulk_create_options(ignore_conflicts=False, update_conflicts=False, update_fields=None, unique_fields=None)
        assert result is None


@pytest.mark.parametrize("ignore_conflicts, update_conflicts, update_fields, unique_fields, exception", [
    (True, True, None, None, ValueError),  
    (True, False, None, None, NotSupportedError),  
    (False, True, None, None, ValueError),  
    (False, True, [], None, ValueError),  
    (False, True, ['username'], [], ValueError),  
])
def test_check_bulk_create_options_exceptions(ignore_conflicts, update_conflicts, update_fields, unique_fields, exception):
    qs = QuerySet(model=User)

    if ignore_conflicts and not connections[qs.db].features.supports_ignore_conflicts:
        with pytest.raises(NotSupportedError):
            qs._check_bulk_create_options(ignore_conflicts=True, update_conflicts=False, update_fields=None, unique_fields=None)
    elif update_conflicts and not connections[qs.db].features.supports_update_conflicts:
        with pytest.raises(NotSupportedError):
            qs._check_bulk_create_options(ignore_conflicts=False, update_conflicts=True, update_fields=update_fields, unique_fields=unique_fields)
    elif update_conflicts and not update_fields:
        with pytest.raises(ValueError):
            qs._check_bulk_create_options(ignore_conflicts=False, update_conflicts=True, update_fields=update_fields, unique_fields=unique_fields)
    elif update_conflicts and unique_fields and not connections[qs.db].features.supports_update_conflicts_with_target:
        with pytest.raises(NotSupportedError):
            qs._check_bulk_create_options(ignore_conflicts=False, update_conflicts=True, update_fields=update_fields, unique_fields=unique_fields)
    elif update_conflicts and not unique_fields:
        with pytest.raises(ValueError):
            qs._check_bulk_create_options(ignore_conflicts=False, update_conflicts=True, update_fields=update_fields, unique_fields=unique_fields)