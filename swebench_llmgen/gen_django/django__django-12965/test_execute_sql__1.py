import pytest
from django.contrib.auth.models import User
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.constants import MULTI, SINGLE, NO_RESULTS, CURSOR

@pytest.fixture
def setup_sql_compiler():
    # Setup a SQLCompiler instance with a User query
    user_query = User.objects.all()
    connection = user_query.model._state.db  # Get the current connection for the User model
    compiler = SQLCompiler(user_query.query, connection)
    return compiler

def test_execute_sql_multi(setup_sql_compiler):
    compiler = setup_sql_compiler
    results = compiler.execute_sql(result_type=MULTI)
    assert isinstance(results, list)  # Should return a list of results
    assert len(results) == User.objects.count()  # Should match the count of User instances

def test_execute_sql_single(setup_sql_compiler):
    compiler = setup_sql_compiler
    results = compiler.execute_sql(result_type=SINGLE)
    assert results is not None  # Should return a single result
    assert isinstance(results, tuple)  # Should return a tuple for the User model

def test_execute_sql_cursor(setup_sql_compiler):
    compiler = setup_sql_compiler
    cursor = compiler.execute_sql(result_type=CURSOR)
    assert cursor is not None  # Should return a cursor
    assert cursor.fetchone() is not None  # Should be able to fetch a row

def test_execute_sql_no_results(setup_sql_compiler):
    compiler = setup_sql_compiler
    # Alter the query to ensure it results in no entries
    compiler.query = compiler.query.filter(pk=-1)  # Filter for a non-existent User
    results = compiler.execute_sql(result_type=NO_RESULTS)
    assert results is None  # Should return None for no results

def test_execute_sql_empty_sql(setup_sql_compiler):
    compiler = setup_sql_compiler
    original_as_sql = compiler.as_sql
    compiler.as_sql = lambda: ("", [])  # Mock as_sql to return empty SQL

    with pytest.raises(EmptyResultSet):
        compiler.execute_sql()
    compiler.as_sql = original_as_sql  # Restore original method