import pytest
from django.db import connection
from django.contrib.auth.models import User
from django.db.models.sql.compiler import SQLCompiler

@pytest.fixture
def setup_query():
    # Prepare a basic query from the User model
    from django.db.models import QuerySet
    queryset = User.objects.all()  # Create a QuerySet instance
    return queryset._query  # Return the underlying query

def test_as_sql_with_limits(setup_query):
    compiler = SQLCompiler(setup_query, connection)
    sql, params = compiler.as_sql()

    # Test for SELECT statement
    assert sql.startswith("SELECT")
    assert 'FROM' in sql
    assert not 'LIMIT' in sql  # No limits yet

def test_as_sql_without_limits(setup_query):
    compiler = SQLCompiler(setup_query, connection)
    sql, params = compiler.as_sql(with_limits=False)

    # Test for SELECT statement
    assert sql.startswith("SELECT")
    assert 'FROM' in sql
    assert 'LIMIT' not in sql  # No limits included

def test_as_sql_with_ordering(setup_query):
    compiler = SQLCompiler(setup_query, connection)
    setup_query.order_by('username')  # Add ordering on username
    sql, params = compiler.as_sql()

    assert "ORDER BY" in sql  # Check that ordering is applied
    assert sql.startswith("SELECT")

def test_as_sql_no_results(setup_query):
    # Test the empty result handling
    from django.db.models.sql.where import EmptyResultSet

    setup_query = setup_query.clone()  # Clone to avoid modifying original
    setup_query.where = EmptyResultSet()  # Simulate empty result

    compiler = SQLCompiler(setup_query, connection)
    
    with pytest.raises(EmptyResultSet):
        compiler.as_sql()

def test_as_sql_with_group_by(setup_query):
    compiler = SQLCompiler(setup_query, connection)
    setup_query.extra_select = [("COUNT(*)", "", "user_count")]  # Add an extra select
    sql, params = compiler.as_sql()

    assert "SELECT COUNT(*) AS user_count" in sql  # Check for count in SQL

def test_as_sql_with_select_for_update(setup_query):
    compiler = SQLCompiler(setup_query, connection)
    setup_query.select_for_update = True  # Set select for update
    sql, params = compiler.as_sql()

    assert "FOR UPDATE" in sql  # Check if FOR UPDATE clause is present
    
def test_as_sql_with_distinct(setup_query):
    compiler = SQLCompiler(setup_query, connection)
    setup_query.distinct = True  # Use DISTINCT
    sql, params = compiler.as_sql()

    assert "SELECT DISTINCT" in sql  # Verify that DISTINCT is in SQL

def test_as_sql_with_full_result_set(setup_query):
    # Create a result set that is full
    from django.db.models.sql.where import FullResultSet

    compiler = SQLCompiler(setup_query, connection)
    
    with pytest.raises(FullResultSet):
        compiler.compile(FullResultSet())  # Simulate a FullResultSet error