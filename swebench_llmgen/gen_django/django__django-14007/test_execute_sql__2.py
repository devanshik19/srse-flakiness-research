import pytest
from django.db import connection
from django.contrib.auth.models import User
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.constants import CURSOR, MULTI, SINGLE

@pytest.fixture
def sql_compiler():
    query = User.objects.all().query
    return SQLCompiler(query, connection)

def test_execute_sql_multi(sql_compiler):
    # Test MULTI result_type
    result = sql_compiler.execute_sql(result_type=MULTI)
    assert isinstance(result, list)
    assert len(result) >= 0  # May be empty but should be a list

def test_execute_sql_single(sql_compiler):
    # Test SINGLE result_type
    result = sql_compiler.execute_sql(result_type=SINGLE)
    if result:
        assert isinstance(result, tuple)
        assert len(result) <= sql_compiler.col_count

def test_execute_sql_cursor(sql_compiler):
    # Test CURSOR result_type
    result = sql_compiler.execute_sql(result_type=CURSOR)
    assert hasattr(result, '__iter__')
    assert callable(result.close)

def test_execute_sql_no_results(sql_compiler):
    # Test NO_RESULTS when query returning no rows
    User.objects.all().delete()  # Ensure no users exist
    result = sql_compiler.execute_sql(result_type=None)
    assert result is None

def test_execute_sql_empty_set(sql_compiler):
    # Mimic a query that generates an empty SQL statement
    sql_compiler.as_sql = lambda: ("", [])
    with pytest.raises(EmptyResultSet):
        sql_compiler.execute_sql(result_type=MULTI)

def test_execute_sql_handle_exception(sql_compiler):
    # Simulate an exception during cursor execution
    sql_compiler.connection.cursor = lambda: 1/0  # Force an exception
    with pytest.raises(Exception):
        sql_compiler.execute_sql(result_type=MULTI)