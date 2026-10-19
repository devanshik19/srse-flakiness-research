import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_count_active_tables_with_active_tables():
    query = Query(User)
    # Simulate adding active tables by manipulating alias_refcount
    query.alias_refcount = {'table1': 1, 'table2': 2, 'table3': 0}
    
    assert query.count_active_tables() == 2

def test_count_active_tables_with_no_active_tables():
    query = Query(User)
    # All tables have a zero reference count
    query.alias_refcount = {'table1': 0, 'table2': 0, 'table3': 0}
    
    assert query.count_active_tables() == 0

def test_count_active_tables_with_empty_alias_refcount():
    query = Query(User)
    # No tables at all
    query.alias_refcount = {}
    
    assert query.count_active_tables() == 0

def test_count_active_tables_with_varied_active_tables():
    query = Query(User)
    # Mixed reference counts
    query.alias_refcount = {'table1': 1, 'table2': 0, 'table3': 3, 'table4': 0, 'table5': 5}
    
    assert query.count_active_tables() == 3