import pytest
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.db.models.sql.query import Query

@pytest.fixture
def user_queryset():
    return User.objects.all()

def test_deferred_to_data_full_loading(user_queryset):
    # Create a Query object with all fields
    query = Query(User)
    query.deferred_loading = ([], False)  # No fields to defer

    target = {}
    query.deferred_to_data(target)
    
    # Assert all fields are included
    assert User in target
    assert {'id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined'} <= target[User]

def test_deferred_to_data_partial_loading(user_queryset):
    # Create a Query object with some fields deferred
    query = Query(User)
    query.deferred_loading = (['username', 'email'], True)  # Defer username and email

    target = {}
    query.deferred_to_data(target)
    
    # Assert deferred fields are not included and required fields are included
    assert User in target
    assert {'id', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined'} <= target[User]
    assert 'username' not in target[User]
    assert 'email' not in target[User]

def test_deferred_to_data_no_fields(user_queryset):
    # Create a Query object with no fields
    query = Query(User)
    query.deferred_loading = ([], False)  # No fields to defer

    target = {}
    query.deferred_to_data(target)
    
    # Assert no fields are added since there's no data
    assert User in target
    assert target[User] == {'id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined'}

def test_deferred_to_data_with_related_fields(user_queryset):
    # Assuming User has related fields (e.g., a profile model, etc.)
    # Create a Query object with some related fields deferred
    query = Query(User)
    query.deferred_loading = (['profile__bio'], True)  # Defer a related field

    target = {}
    query.deferred_to_data(target)
    
    # Assert that related fields are not included
    assert User in target
    assert {'id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined'} <= target[User]
    assert 'profile__bio' not in target[User]