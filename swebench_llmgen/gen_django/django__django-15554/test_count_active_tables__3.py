import pytest
from django.db.models.sql.query import Query
from django.contrib.auth.models import User

def test_count_active_tables():
    # Create a Query object with active and inactive tables
    query = Query(model=User, alias_cols={})

    # Simulate some alias reference counts for testing
    query.alias_refcount = {
        'user': 1,          # Active table
        'group': 0,         # Inactive table
        'session': 3,       # Active table
        'auth_user': 0      # Inactive table
    }

    # Verify that it counts only active tables
    assert query.count_active_tables() == 2  # user and session are active

    # Change alias_refcount to have all inactive entries
    query.alias_refcount = {
        'user': 0,
        'group': 0,
        'session': 0,
        'auth_user': 0
    }
    
    # Now it should return zero active tables
    assert query.count_active_tables() == 0

    # Test with a single active table
    query.alias_refcount = {
        'user': 1
    }
    assert query.count_active_tables() == 1

    # Test with no tables
    query.alias_refcount = {}
    assert query.count_active_tables() == 0