import pytest
from django.contrib.auth.models import User
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.constants import MULTI, SINGLE, NO_RESULTS, CURSOR

@pytest.fixture
def sql_compiler():
    # Assuming a simple setup for the SQLCompiler. This might need adaptation
    # depending on the actual implementation details of the other required fields.
    user = User.objects.create(username='testuser', password='password')
    query = user.objects.all()
    connection = user._state.db  # Use the default database connection
    return SQLCompiler(query, connection, using='default')

def test_execute_sql_multi(sql_compiler):
    result = sql_compiler.execute_sql(result_type=MULTI)
    assert isinstance(result, list)  # Ensure it returns a list.
    assert len(result) > 0  # There should be results since the User table is populated.

def test_execute_sql_single(sql_compiler):
    result = sql_compiler.execute_sql(result_type=SINGLE)
    assert isinstance(result, tuple)  # Ensure it returns a single row as a tuple.
    assert len(result) == 1  # There should be one result in the tuple.

def test_execute_sql_cursor(sql_compiler):
    cursor = sql_compiler.execute_sql(result_type=CURSOR)
    assert cursor is not None  # Ensure cursor is returned.
    cursor.close()  # Clean up the cursor after use.

def test_execute_sql_no_results(sql_compiler):
    # Set up a compiler with a query that would not return results
    sql_compiler.query = sql_compiler.query.filter(username='nonexistentuser')
    result = sql_compiler.execute_sql(result_type=NO_RESULTS)
    assert result is None  # Expect None when no results.

def test_execute_sql_empty_query(sql_compiler):
    # Simulating an empty query scenario
    sql_compiler.as_sql = lambda: ("", [])
    with pytest.raises(EmptyResultSet):
        sql_compiler.execute_sql(result_type=MULTI)