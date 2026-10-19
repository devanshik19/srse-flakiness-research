import pytest
from django.contrib.auth.models import User
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query
from django.db import connection

@pytest.fixture
def user_query():
    query = Query(User)
    return query

@pytest.fixture
def sql_compiler(user_query):
    return SQLCompiler(query=user_query, connection=connection, using='', elide_empty=False)

def test_as_sql_with_limits(sql_compiler):
    sql, params = sql_compiler.as_sql(with_limits=True)
    assert sql.startswith("SELECT")
    assert "FROM" in sql
    assert params == ()

def test_as_sql_without_limits(sql_compiler):
    sql, params = sql_compiler.as_sql(with_limits=False)
    assert sql.startswith("SELECT")
    assert "FROM" in sql
    assert params == ()

def test_as_sql_with_col_aliases(sql_compiler):
    sql_compiler.select = [(Value('id'), [], 'user_id')]
    sql, params = sql_compiler.as_sql(with_limits=True, with_col_aliases=True)
    assert "AS user_id" in sql
    assert "SELECT" in sql

def test_as_sql_full_result_set(sql_compiler):
    sql_compiler.where = None
    sql, params = sql_compiler.as_sql()
    assert "WHERE" not in sql

def test_as_sql_empty_result_set(sql_compiler):
    sql_compiler.where = None
    sql_compiler.elide_empty = True
    with pytest.raises(Exception):
        sql_compiler.as_sql()

def test_as_sql_with_group_by(sql_compiler):
    sql_compiler.ordering_parts = ["username"]
    sql, params = sql_compiler.as_sql(with_limits=True)
    assert "ORDER BY" in sql

def test_as_sql_with_distinct(sql_compiler):
    sql_compiler.query.distinct = True
    sql, params = sql_compiler.as_sql()
    assert "DISTINCT" in sql

def test_as_sql_with_having(sql_compiler):
    sql_compiler.having = sql_compiler.compile(None)  # Simulate having clause
    sql, params = sql_compiler.as_sql()
    assert "HAVING" in sql