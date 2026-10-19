import pytest
from django.contrib.auth.models import User
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query

def test_as_sql_with_limits():
    # Setup
    query = Query(User)
    query.add_fields(['username', 'email'])
    query.set_limits(0, 10)
    compiler = SQLCompiler(query, query.get_connection())

    # Execute
    sql, params = compiler.as_sql(with_limits=True)

    # Assert
    assert sql.startswith("SELECT")
    assert "LIMIT" in sql

def test_as_sql_without_limits():
    # Setup
    query = Query(User)
    query.add_fields(['username', 'email'])
    query.set_limits(None, None)
    compiler = SQLCompiler(query, query.get_connection())

    # Execute
    sql, params = compiler.as_sql(with_limits=False)

    # Assert
    assert sql.startswith("SELECT")
    assert "LIMIT" not in sql

def test_as_sql_with_group_by():
    # Setup
    query = Query(User)
    query.add_fields(['username', 'email'])
    query.add_order_by('username')
    query.add_group_by('email')
    compiler = SQLCompiler(query, query.get_connection())

    # Execute
    sql, params = compiler.as_sql(with_limits=True)

    # Assert
    assert "GROUP BY" in sql

def test_as_sql_with_distinct():
    # Setup
    query = Query(User)
    query.add_fields(['username', 'email'])
    query.distinct = True
    compiler = SQLCompiler(query, query.get_connection())

    # Execute
    sql, params = compiler.as_sql(with_limits=True)

    # Assert
    assert "DISTINCT" in sql

def test_as_sql_empty_result():
    # Setup
    query = Query(User)
    query.add_fields(['username', 'email'])
    query.where = query.where.add(('username', 'nonexistent_user'), 'AND')
    compiler = SQLCompiler(query, query.get_connection())

    # Execute
    sql, params = compiler.as_sql(with_limits=False)

    # Assert
    assert sql.startswith("SELECT")
    assert "0 = 1" in sql  # Check for elided empty result

def test_as_sql_with_explain():
    # Setup
    query = Query(User)
    query.add_fields(['username', 'email'])
    query.explain_info = True  # Simulating an explain query
    compiler = SQLCompiler(query, query.get_connection())

    # Execute
    sql, params = compiler.as_sql(with_limits=True)

    # Assert
    assert sql.startswith("EXPLAIN")