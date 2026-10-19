import pytest
from django.db.models.sql.query import Query
from django.contrib.auth.models import User

def test_count_active_tables():
    # Create a Query instance
    query = Query(User)

    # Manually set alias_refcount to simulate active tables
    query.alias_refcount = {'a': 1, 'b': 2, 'c': 0}  # Expecting 3 active tables

    # Check if count_active_tables returns the correct number of active tables
    assert query.count_active_tables() == 3

    # Change the reference counts and test again
    query.alias_refcount = {'a': 0, 'b': 0, 'c': 0}  # Expecting 0 active tables
    assert query.count_active_tables() == 0

    query.alias_refcount = {'a': 1}  # Expecting 1 active table
    assert query.count_active_tables() == 1