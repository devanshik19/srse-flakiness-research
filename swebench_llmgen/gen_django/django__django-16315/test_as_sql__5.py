import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query

@pytest.fixture
def user_query():
    query = Query(User)
    query.add_filter('is_active', True)
    return query

def test_as_sql_no_limits(user_query):
    compiler = SQLCompiler(query=user_query, connection=connection, using=None, elide_empty=False)
    sql, params = compiler.as_sql(with_limits=False)
    
    assert sql.startswith("SELECT")
    assert "FROM" in sql
    assert "WHERE" in sql
    assert params == []

def test_as_sql_with_limits(user_query):
    compiler = SQLCompiler(query=user_query, connection=connection, using=None, elide_empty=False)
    sql, params = compiler.as_sql(with_limits=True)

    assert sql.startswith("SELECT")
    assert "LIMIT" in sql or "OFFSET" in sql

def test_as_sql_with_ordering(user_query):
    user_query.order_by = ['username']
    compiler = SQLCompiler(query=user_query, connection=connection, using=None, elide_empty=False)
    sql, params = compiler.as_sql()
    
    assert "ORDER BY" in sql
    assert "username" in sql

def test_as_sql_with_group_by(user_query):
    user_query.group_by = ['date_joined']
    compiler = SQLCompiler(query=user_query, connection=connection, using=None, elide_empty=False)
    sql, params = compiler.as_sql()
    
    assert "GROUP BY" in sql
    assert "date_joined" in sql

def test_as_sql_empty_result_set(user_query):
    user_query.add_filter('id', -1)  # Assuming no user with id -1
    compiler = SQLCompiler(query=user_query, connection=connection, using=None, elide_empty=True)
    
    with pytest.raises(EmptyResultSet):
        compiler.as_sql()

def test_as_sql_full_result_set(user_query):
    user_query.add_filter('username', 'non_existent_user')  # No user with this username
    compiler = SQLCompiler(query=user_query, connection=connection, using=None, elide_empty=False)
    sql, params = compiler.as_sql()
    
    assert "WHERE" in sql
    assert params == ['non_existent_user']