import pytest
from django.contrib.auth.models import User
from django.db import connections, NotSupportedError
from django.db.models import OnConflict

@pytest.fixture
def queryset():
    from django.db.models.query import QuerySet
    return QuerySet(model=User, query=None, using=None, hints=None)

def test_check_bulk_create_options_ignore_conflicts(queryset):
    result = queryset._check_bulk_create_options(True, False, None, None)
    assert result == OnConflict.IGNORE

def test_check_bulk_create_options_update_conflicts(queryset):
    # Test with update_conflicts without unique_fields
    with pytest.raises(ValueError, match="Fields that will be updated when a row insertion fails"):
        queryset._check_bulk_create_options(False, True, [], None)

    # Test with database feature not supporting update conflicts
    connections[queryset.db].features.supports_update_conflicts = False
    with pytest.raises(NotSupportedError, match="This database backend does not support updating conflicts."):
        queryset._check_bulk_create_options(False, True, ['field1'], ['unique_field'])

    # Test with valid update_conflicts
    connections[queryset.db].features.supports_update_conflicts = True
    result = queryset._check_bulk_create_options(False, True, ['username'], ['email'])
    assert result == OnConflict.UPDATE

def test_check_bulk_create_options_exclusive_flags(queryset):
    with pytest.raises(ValueError, match="ignore_conflicts and update_conflicts are mutually exclusive."):
        queryset._check_bulk_create_options(True, True, None, None)

def test_check_bulk_create_options_unique_fields_validation(queryset):
    connections[queryset.db].features.supports_update_conflicts = True
    connections[queryset.db].features.supports_update_conflicts_with_target = True

    # Test with empty unique_fields if supports_update_conflicts_with_target is True
    with pytest.raises(ValueError, match="Unique fields that can trigger the upsert must be provided."):
        queryset._check_bulk_create_options(False, True, ['username'], None)

    # Test with unique_fields that are not concrete
    with pytest.raises(ValueError, match="bulk_create() can only be used with concrete fields in unique_fields."):
        queryset._check_bulk_create_options(False, True, ['username'], ['non_concrete_field'])

    # Test with valid unique_fields
    result = queryset._check_bulk_create_options(False, True, ['username'], ['email'])
    assert result == OnConflict.UPDATE

def test_check_bulk_create_options_multiple_conditions(queryset):
    connections[queryset.db].features.supports_update_conflicts = True
    connections[queryset.db].features.supports_update_conflicts_with_target = True

    # Validate for concrete fields for update_fields
    with pytest.raises(ValueError, match="bulk_create() can only be used with concrete fields in update_fields."):
        queryset._check_bulk_create_options(False, True, ['field1_non_concrete'], ['unique_field'])

    # Validate for primary keys in update_fields
    with pytest.raises(ValueError, match="bulk_create() cannot be used with primary keys in update_fields."):
        queryset._check_bulk_create_options(False, True, ['id'], ['unique_field'])

    result = queryset._check_bulk_create_options(False, True, ['username'], ['email'])
    assert result == OnConflict.UPDATE