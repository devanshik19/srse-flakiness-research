import pytest
from django.contrib.auth.models import User
from django.db import NotSupportedError, IntegrityError
from django.db.models.query import QuerySet

@pytest.fixture
def user_queryset():
    return User.objects

def test_check_bulk_create_options_ignore_conflicts(user_queryset):
    assert user_queryset._check_bulk_create_options(True, False, None, None) == OnConflict.IGNORE

def test_check_bulk_create_options_update_conflicts_without_update_fields(user_queryset):
    with pytest.raises(ValueError, match="Fields that will be updated when a row insertion fails"):
        user_queryset._check_bulk_create_options(False, True, None, None)

def test_check_bulk_create_options_update_conflicts_with_primary_key(user_queryset):
    with pytest.raises(ValueError, match="bulk_create() cannot be used with primary keys in update_fields."):
        user_queryset._check_bulk_create_options(False, True, ['id'], None)

def test_check_bulk_create_options_update_conflicts_with_non_concrete_field(user_queryset):
    with pytest.raises(ValueError, match="bulk_create() can only be used with concrete fields in update_fields."):
        user_queryset._check_bulk_create_options(False, True, ['username'], None)

def test_check_bulk_create_options_update_conflicts_with_unique_fields_without_target(user_queryset):
    with pytest.raises(ValueError, match="Unique fields that can trigger the upsert must be provided."):
        user_queryset._check_bulk_create_options(False, True, ['username'], None)

def test_check_bulk_create_options_no_conflicts(user_queryset):
    assert user_queryset._check_bulk_create_options(False, False, None, None) is None

def test_check_bulk_create_options_not_supported_ignore_conflicts(user_queryset):
    with pytest.raises(NotSupportedError, match="This database backend does not support ignoring conflicts."):
        user_queryset._check_bulk_create_options(True, False, None, None)

def test_check_bulk_create_options_not_supported_update_conflicts(user_queryset):
    with pytest.raises(NotSupportedError, match="This database backend does not support updating conflicts."):
        user_queryset._check_bulk_create_options(False, True, ['username'], None)