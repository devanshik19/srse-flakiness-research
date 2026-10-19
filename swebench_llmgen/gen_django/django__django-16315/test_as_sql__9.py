import pytest
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query
from django.db import connections
from django.contrib.auth.models import User

def test_as_sql_with_limits():
    query = Query(User)
    query.add_columns(['id', 'username'])
    query.set_limits(0, 10)
    compiler = SQLCompiler(query, connections['default'], using='default')
    
    sql, params = compiler.as_sql(with_limits=True)
    
    assert "SELECT id, username" in sql
    assert "FROM" in sql
    assert "LIMIT 10" in sql

def test_as_sql_without_limits():
    query = Query(User)
    query.add_columns(['id', 'username'])
    compiler = SQLCompiler(query, connections['default'], using='default')
    
    sql, params = compiler.as_sql(with_limits=False)
    
    assert "SELECT id, username" in sql
    assert "FROM" in sql
    assert "LIMIT" not in sql

def test_as_sql_with_distinct():
    query = Query(User)
    query.add_columns(['id', 'username'])
    query.distinct = True
    compiler = SQLCompiler(query, connections['default'], using='default')
    
    sql, params = compiler.as_sql()
    
    assert "SELECT DISTINCT" in sql

def test_as_sql_with_group_by():
    query = Query(User)
    query.add_columns(['id', 'username'])
    query.group_by = ['username']
    compiler = SQLCompiler(query, connections['default'], using='default')
    
    sql, params = compiler.as_sql()
    
    assert "GROUP BY username" in sql

def test_as_sql_empty_result_set():
    query = Query(User)
    query.set_limits(0, 1)
    query.where = "id = -1"  # Condition that yields no results

    compiler = SQLCompiler(query, connections['default'], using='default')

    with pytest.raises(Exception):  # This should typically raise EmptyResultSet
        compiler.as_sql()

def test_as_sql_order_by():
    query = Query(User)
    query.add_columns(['id', 'username'])
    query.order_by = [('username', 'ASC')]
    compiler = SQLCompiler(query, connections['default'], using='default')

    sql, params = compiler.as_sql()

    assert "ORDER BY username ASC" in sql