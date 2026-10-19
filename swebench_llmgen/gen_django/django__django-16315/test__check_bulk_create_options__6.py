import pytest
from django.db import NotSupportedError
from django.contrib.auth.models import User
from django.db.models.query import QuerySet

@pytest.mark.parametrize(
    "ignore_conflicts, update_conflicts, update_fields, unique_fields, expected_result, expected_exception",
    [
        (True, False, None, None, None, None),  # Ignore conflicts, expect OnConflict.IGNORE
        (False, True, ['username'], ['email'], None, None),  # Update conflicts, expect OnConflict.UPDATE
        (True, True, None, None, None, ValueError),  # Both true, expect ValueError
        (True, False, None, None, None, None),  # Ignore conflicts
        (False, True, None, None, None, ValueError),  # Update conflicts without fields
        (False, True, ['username'], None, None, ValueError),  # No unique fields provided
    ]
)
def test_check_bulk_create_options(ignore_conflicts, update_conflicts, update_fields, unique_fields, expected_result, expected_exception):
    qs = QuerySet(model=User)  # Initialize QuerySet with User model

    if expected_exception:
        with pytest.raises(expected_exception):
            qs._check_bulk_create_options(ignore_conflicts, update_conflicts, update_fields, unique_fields)
    else:
        result = qs._check_bulk_create_options(ignore_conflicts, update_conflicts, update_fields, unique_fields)
        assert result == expected_result