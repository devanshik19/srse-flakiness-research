import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_count_active_tables():
    # Create a query instance for the User model
    query = Query(User)

    # Simulate some alias reference counts
    query.alias_refcount = {
        'users': 1,
        'groups': 0,
        'permissions': 2,
    }

    # Test when there are active tables
    active_table_count = query.count_active_tables()
    assert active_table_count == 3  # 'users' (1), 'groups' (0), 'permissions' (2)

    # Now clear the alias_refcount and test again
    query.alias_refcount = {
        'users': 0,
        'groups': 0,
        'permissions': 0,
    }
    active_table_count_zero = query.count_active_tables()
    assert active_table_count_zero == 0  # All reference counts are zero