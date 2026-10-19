import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query

@pytest.fixture
def setup_query():
    user = User.objects.create(username='testuser', password='password123')
    query = Query(User)
    query.add_deferred_loading(['username'])  # Assume 'username' is a field we want to defer
    return query

def test_deferred_to_data_with_deferred_fields(setup_query):
    target = {}
    query = setup_query
    query.deferred_to_data(target)
    
    assert 'auth.User' in target
    assert target['auth.User'] == {'id', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined'}

def test_deferred_to_data_without_deferred_fields(setup_query):
    target = {}
    query = setup_query
    query.clear_deferred_loading()  # Clear any deferred loading
    query.deferred_to_data(target)
    
    assert 'auth.User' in target
    assert target['auth.User'] == {'id', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined'}

def test_deferred_to_data_with_no_fields(setup_query):
    target = {}
    query = setup_query
    query.add_deferred_loading([])  # Empty deferred loading
    query.deferred_to_data(target)
    
    assert target == {}