import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.constants import MULTI, SINGLE, CURSOR, NO_RESULTS

@pytest.fixture
def sql_compiler():
    # This fixture initializes an SQLCompiler instance.
    # Assuming you have a query object already set up.
    query = User.objects.all().query
    return SQLCompiler(query, connection)

def test_execute_sql_multi(sql_compiler):
    result = sql_compiler.execute_sql(result_type=MULTI)
    assert isinstance(result, list)
    assert all(isinstance(user, User) for user in result)

def test_execute_sql_single(sql_compiler):
    # To test SINGLE, we need to ensure there's at least one User
    user = User.objects.first()
    assert user is not None  # Assure there's at least one user
    result = sql_compiler.execute_sql(result_type=SINGLE)
    assert isinstance(result, User)
    assert result == user

def test_execute_sql_cursor(sql_compiler):
    result = sql_compiler.execute_sql(result_type=CURSOR)
    assert result is not None
    assert hasattr(result, 'fetchone')  # ensure it's a cursor
    row = result.fetchone()
    assert isinstance(row, tuple)  # ensure it returns tuples

def test_execute_sql_no_results(sql_compiler):
    # Assuming a condition where there are no users
    # Clear all users for this test
    User.objects.all().delete()
    result = sql_compiler.execute_sql(result_type=NO_RESULTS)
    assert result is None  # should return None for NO_RESULTS

def test_execute_sql_empty_result_set(sql_compiler):
    # Simulate an empty result set without hitting the database
    sql_compiler.as_sql = lambda: ("", [])
    with pytest.raises(EmptyResultSet):
        sql_compiler.execute_sql(result_type=MULTI)

def test_execute_sql_chunked_fetch(sql_compiler):
    result = sql_compiler.execute_sql(chunked_fetch=True)
    assert isinstance(result, list)  # should return as list even in chunked
    assert all(isinstance(user, User) for user in result)