import pytest
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.db.utils import IntegrityError, NotSupportedError

@pytest.fixture
def user_queryset():
    return User.objects.all()

def test_check_bulk_create_options_ignore_conflicts(user_queryset):
    qs = user_queryset._clone()  # Create a clone of the QuerySet

    # Test when both ignore_conflicts and update_conflicts are set
    with pytest.raises(ValueError, match="mutually exclusive"):
        qs._check_bulk_create_options(ignore_conflicts=True, update_conflicts=True, update_fields=None, unique_fields=None)

    # Test when ignore_conflicts is True but database does not support it
    qs.db = 'dummy_db'  # Set a dummy db name
    with pytest.raises(NotSupportedError, match="ignoring conflicts"):
        qs._check_bulk_create_options(ignore_conflicts=True, update_conflicts=False, update_fields=None, unique_fields=None)

    # Test when ignore_conflicts is True and supports it
    qs.db = 'default'  # Reset to valid db
    from django.db import connections
    connections[qs.db].features.supports_ignore_conflicts = True
    assert qs._check_bulk_create_options(ignore_conflicts=True, update_conflicts=False, update_fields=None, unique_fields=None) == OnConflict.IGNORE

def test_check_bulk_create_options_update_conflicts(user_queryset):
    qs = user_queryset._clone()

    # Test when update_conflicts is True but fields are not provided
    with pytest.raises(ValueError, match="must be provided"):
        qs._check_bulk_create_options(ignore_conflicts=False, update_conflicts=True, update_fields=[], unique_fields=None)

    # Test without unique_fields when it is required by database
    with pytest.raises(ValueError, match="must be provided"):
        qs._check_bulk_create_options(ignore_conflicts=False, update_conflicts=True, update_fields=["username"], unique_fields=None)

    # Test when update_conflicts is True but database does not support it
    qs.db = 'dummy_db'
    with pytest.raises(NotSupportedError, match="updating conflicts"):
        qs._check_bulk_create_options(ignore_conflicts=False, update_conflicts=True, update_fields=["username"], unique_fields=["id"])

    # Test with valid update_conflicts and unique_fields setup
    qs.db = 'default'
    connections[qs.db].features.supports_update_conflicts = True
    connections[qs.db].features.supports_update_conflicts_with_target = True
    assert qs._check_bulk_create_options(ignore_conflicts=False, update_conflicts=True, update_fields=["username"], unique_fields=["id"]) == OnConflict.UPDATE
    
    # Check when provided fields are not concrete or are primary keys
    with pytest.raises(ValueError, match="cannot be used with primary keys"):
        qs._check_bulk_create_options(ignore_conflicts=False, update_conflicts=True, update_fields=["id"], unique_fields=["username"])

    # Ensure proper response for valid concrete fields
    connections[qs.db].features.supports_update_conflicts_with_target = True
    User._meta.get_field = lambda x: User._meta.fields[0] if x == 'username' else User._meta.fields[1]  # Simplified for demonstration
    assert qs._check_bulk_create_options(ignore_conflicts=False, update_conflicts=True, update_fields=["username"], unique_fields=["id"]) == OnConflict.UPDATE