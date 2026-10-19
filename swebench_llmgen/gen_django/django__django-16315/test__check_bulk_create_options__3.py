import pytest
from django.contrib.auth.models import User
from django.db import connections
from django.db.models import QuerySet
from django.db.models.constants import OnConflict
from django.core.exceptions import NotSupportedError

@pytest.fixture
def queryset():
    return QuerySet(model=User, query=None)

def test_check_bulk_create_options_ignore_conflicts(queryset):
    # Test ignore_conflicts without database support
    connections[queryset.db].features.supports_ignore_conflicts = False
    with pytest.raises(NotSupportedError) as excinfo:
        queryset._check_bulk_create_options(ignore_conflicts=True, update_conflicts=False, update_fields=None, unique_fields=None)
    assert str(excinfo.value) == "This database backend does not support ignoring conflicts."

def test_check_bulk_create_options_update_conflicts(queryset):
    # Test update_conflicts without database support
    connections[queryset.db].features.supports_update_conflicts = False
    with pytest.raises(NotSupportedError) as excinfo:
        queryset._check_bulk_create_options(ignore_conflicts=False, update_conflicts=True, update_fields=["username"], unique_fields=None)
    assert str(excinfo.value) == "This database backend does not support updating conflicts."

def test_check_bulk_create_options_update_fields_required(queryset):
    connections[queryset.db].features.supports_update_conflicts = True
    with pytest.raises(ValueError) as excinfo:
        queryset._check_bulk_create_options(ignore_conflicts=False, update_conflicts=True, update_fields=[], unique_fields=None)
    assert str(excinfo.value) == "Fields that will be updated when a row insertion fails on conflicts must be provided."

def test_check_bulk_create_options_unique_fields_required_when_upsert(queryset):
    connections[queryset.db].features.supports_update_conflicts = True
    connections[queryset.db].features.supports_update_conflicts_with_target = True
    with pytest.raises(ValueError) as excinfo:
        queryset._check_bulk_create_options(ignore_conflicts=False, update_conflicts=True, update_fields=["username"], unique_fields=None)
    assert str(excinfo.value) == "Unique fields that can trigger the upsert must be provided."

def test_check_bulk_create_options_concrete_fields_only(queryset):
    connections[queryset.db].features.supports_update_conflicts = True
    connections[queryset.db].features.supports_update_conflicts_with_target = True
    fields = ["username"]
    
    with pytest.raises(ValueError) as excinfo:
        queryset._check_bulk_create_options(
            ignore_conflicts=False,
            update_conflicts=True,
            update_fields=fields,
            unique_fields=fields
        )
    assert str(excinfo.value) == "bulk_create() can only be used with concrete fields in update_fields."

def test_check_bulk_create_options_successful_case(queryset):
    connections[queryset.db].features.supports_ignore_conflicts = True
    connections[queryset.db].features.supports_update_conflicts = True
    connections[queryset.db].features.supports_update_conflicts_with_target = True
    
    result = queryset._check_bulk_create_options(False, True, ["username"], ["email"])
    assert result == OnConflict.UPDATE

    result = queryset._check_bulk_create_options(True, False, None, None)
    assert result == OnConflict.IGNORE