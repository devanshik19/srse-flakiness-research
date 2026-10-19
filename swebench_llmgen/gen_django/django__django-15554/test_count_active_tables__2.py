import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_count_active_tables():
    # Create a Query instance on User
    query = Query(User)

    # Check initial count of active tables (should be 0)
    assert query.count_active_tables() == 0

    # Simulate having references by manually adjusting alias_refcount
    query.alias_refcount = {'alias_1': 1, 'alias_2': 0, 'alias_3': 2}

    # Check count of active tables (should be 3, since alias_1 and alias_3 have non-zero counts)
    assert query.count_active_tables() == 2

    # Reset the reference counts to simulate cleanup
    query.alias_refcount = {'alias_1': 0, 'alias_2': 0, 'alias_3': 0}

    # Check the count again (should be 0)
    assert query.count_active_tables() == 0