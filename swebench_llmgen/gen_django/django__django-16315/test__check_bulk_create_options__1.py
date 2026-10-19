import pytest
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.db import connections, NotSupportedError

@pytest.mark.parametrize(
    "ignore_conflicts, update_conflicts, update_fields, unique_fields, expected_result, expected_exception",
    [
        (True, False, None, None, OnConflict.IGNORE, None),
        (False, True, ["username"], ["email"], OnConflict.UPDATE, None),
        (False, True, None, ["email"], None, ValueError),
        (False, True, ["username"], None, None, ValueError),
        (False, True, ["username"], ["email"], OnConflict.UPDATE, None),
        (True, True, None, None, None, ValueError),
        (False, True, ["username"], ["nonexistent_field"], None, NotSupportedError),
    ]
)
def test_check_bulk_create_options(ignore_conflicts, update_conflicts, update_fields, unique_fields, expected_result, expected_exception):
    queryset = QuerySet(model=User)

    if expected_exception is not None:
        with pytest.raises(expected_exception):
            queryset._check_bulk_create_options(ignore_conflicts, update_conflicts, update_fields, unique_fields)
    else:
        result = queryset._check_bulk_create_options(ignore_conflicts, update_conflicts, update_fields, unique_fields)
        assert result == expected_result