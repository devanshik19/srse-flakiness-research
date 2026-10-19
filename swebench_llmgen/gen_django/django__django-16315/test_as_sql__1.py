import pytest
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query
from django.contrib.auth.models import User
from django.db import connection

@pytest.mark.parametrize("with_limits, expected_sql", [
    (True, "SELECT * FROM auth_user WHERE 0 = 1"),
    (False, "SELECT * FROM auth_user"),
])
def test_as_sql_with_empty_query(with_limits, expected_sql):
    # Create a Query object targeting the User model
    query = Query(User._meta)
    compiler = SQLCompiler(query, connection)
    
    # Set up a simple query with a where clause that results in no results
    query.add_filter(('username', 'exact'), 'nonexistent_user')

    # Call as_sql and capture the result
    sql, params = compiler.as_sql(with_limits=with_limits)

    assert sql.strip() == expected_sql
    assert params == []

def test_as_sql_with_limit_offset():
    query = Query(User._meta)
    compiler = SQLCompiler(query, connection)
    
    # Set up a query with limit and offset
    query.low_mark = 0
    query.high_mark = 10
    query.add_order_by(('username',))

    sql, params = compiler.as_sql()

    assert "LIMIT" in sql
    assert "OFFSET" in sql

def test_as_sql_with_select_for_update():
    query = Query(User._meta)
    query.select_for_update = True
    compiler = SQLCompiler(query, connection)

    sql, params = compiler.as_sql(with_limits=False)

    assert "FOR UPDATE" in sql