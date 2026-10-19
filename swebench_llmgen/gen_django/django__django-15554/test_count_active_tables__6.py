import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def query_with_active_tables():
    # Create a sample Query object
    query = Query(model=User)

    # Simulating some active tables by manipulating alias_refcount
    query.alias_refcount = {
        'a': 1,  # Active
        'b': 0,  # Inactive
        'c': 2,  # Active
    }
    return query

def test_count_active_tables(query_with_active_tables):
    # Test count_active_tables for active references
    assert query_with_active_tables.count_active_tables() == 2

def test_count_active_tables_no_active_tables():
    query = Query(model=User)
    query.alias_refcount = {'a': 0, 'b': 0}
    assert query.count_active_tables() == 0

def test_count_active_tables_all_active_tables():
    query = Query(model=User)
    query.alias_refcount = {'a': 1, 'b': 1, 'c': 1}
    assert query.count_active_tables() == 3

def test_count_active_tables_mixed_tables():
    query = Query(model=User)
    query.alias_refcount = {'a': 1, 'b': 0, 'c': 1, 'd': 0, 'e': 2}
    assert query.count_active_tables() == 3