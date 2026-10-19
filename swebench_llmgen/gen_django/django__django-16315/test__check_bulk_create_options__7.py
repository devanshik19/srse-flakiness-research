import pytest
from django.contrib.auth.models import User
from django.db import connections
from django.db.models import OnConflict
from django.db.models.query import QuerySet
from django.db.models import NotSupportedError

@pytest.mark.parametrize("ignore_conflicts, update_conflicts, update_fields, unique_fields, expected", [
    (True, False, [], [], OnConflict.IGNORE),
    (False, True, ['username'], ['email'], OnConflict.UPDATE),
    (False, False, [], [], None),
])
def test_check_bulk_create_options_valid_cases(ignore_conflicts, update_conflicts, update_fields, unique_fields, expected):
    queryset = QuerySet(model=User)

    result = queryset._check_bulk_create_options(ignore_conflicts, update_conflicts, update_fields, unique_fields)
    assert result is expected

def test_check_bulk_create_options_ignore_conflicts_and_update_conflicts():
    queryset = QuerySet(model=User)
    with pytest.raises(ValueError, match="mutually exclusive"):
        queryset._check_bulk_create_options(True, True, [], [])

def test_check_bulk_create_options_ignore_conflicts_not_supported():
    queryset = QuerySet(model=User)
    connections[queryset.db].features.supports_ignore_conflicts = False
    with pytest.raises(NotSupportedError, match="does not support ignoring conflicts"):
        queryset._check_bulk_create_options(True, False, [], [])

def test_check_bulk_create_options_update_conflicts_not_supported():
    queryset = QuerySet(model=User)
    connections[queryset.db].features.supports_update_conflicts = False
    with pytest.raises(NotSupportedError, match="does not support updating conflicts"):
        queryset._check_bulk_create_options(False, True, ['username'], [])

def test_check_bulk_create_options_update_conflicts_no_update_fields():
    queryset = QuerySet(model=User)
    with pytest.raises(ValueError, match="must be provided"):
        queryset._check_bulk_create_options(False, True, [], [])

def test_check_bulk_create_options_update_conflicts_no_unique_fields():
    queryset = QuerySet(model=User)
    connections[queryset.db].features.supports_update_conflicts_with_target = True
    with pytest.raises(ValueError, match="must be provided"):
        queryset._check_bulk_create_options(False, True, ['username'], [])

def test_check_bulk_create_options_update_fields_primary_key():
    queryset = QuerySet(model=User)
    with pytest.raises(ValueError, match="cannot be used with primary keys"):
        queryset._check_bulk_create_options(False, True, ['id'], [])

def test_check_bulk_create_options_update_fields_non_concrete():
    queryset = QuerySet(model=User)
    with pytest.raises(ValueError, match="can only be used with concrete fields"):
        queryset._check_bulk_create_options(False, True, ['last_login'], [])

def test_check_bulk_create_options_unique_fields_non_concrete():
    queryset = QuerySet(model=User)
    with pytest.raises(ValueError, match="can only be used with concrete fields"):
        queryset._check_bulk_create_options(False, True, ['username'], ['last_login'])