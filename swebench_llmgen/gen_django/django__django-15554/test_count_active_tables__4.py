import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_count_active_tables():
    # Create a Query instance
    query = Query(User)
    
    # Initially, no aliases should have a reference count
    assert query.count_active_tables() == 0
    
    # Simulate adding an alias with a non-zero reference count
    query.alias_refcount = {'auth_user': 1}  # Manually set reference count for the 'User' model
    assert query.count_active_tables() == 1
    
    # Add another alias with a non-zero reference count
    query.alias_refcount['auth_user_2'] = 2  # Another alias with reference count
    assert query.count_active_tables() == 2
    
    # Remove the first alias
    del query.alias_refcount['auth_user']
    assert query.count_active_tables() == 1
    
    # Set it back to zero
    query.alias_refcount['auth_user_2'] = 0
    assert query.count_active_tables() == 0
    
    # Add multiple aliases with one active
    query.alias_refcount = {'auth_user_3': 1, 'auth_user_4': 0}
    assert query.count_active_tables() == 1
    
    # Check when count is empty
    query.alias_refcount = {}
    assert query.count_active_tables() == 0