import pytest
from django.contrib.auth.models import User
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.constants import MULTI, SINGLE, CURSOR, NO_RESULTS
from django.db.utils import OperationalError

@pytest.fixture
def sql_compiler(db):
    # Create a mock SQLCompiler for testing with an empty query.
    query = User.objects.all()  # Using Django's User model for a valid query context
    connection = User.objects.db.connection
    return SQLCompiler(query.query, connection, using='default')

def test_execute_sql_multi(sql_compiler):
    results = sql_compiler.execute_sql(result_type=MULTI)
    assert isinstance(results, list)  # Ensure it returns a list
    assert len(results) == User.objects.count()  # Length should match the User table count

def test_execute_sql_single(sql_compiler):
    user = User.objects.create(username='testuser')
    sql_compiler.setup_query()
    result = sql_compiler.execute_sql(result_type=SINGLE)
    assert result == (user.id, user.username)  # Adjust based on the expected result structure

def test_execute_sql_cursor(sql_compiler):
    cursor = sql_compiler.execute_sql(result_type=CURSOR)
    assert cursor is not None  # Ensure a cursor is returned
    assert hasattr(cursor, 'fetchone')  # Check cursor has fetchone method
    cursor.close()  # Clean up cursor

def test_execute_sql_no_results(sql_compiler):
    User.objects.all().delete()  # Delete all users to simulate no results
    result = sql_compiler.execute_sql(result_type=NO_RESULTS)
    assert result is None  # Should return None for no results

def test_execute_sql_empty_query(sql_compiler):
    sql_compiler.as_sql = lambda: ("", [])  # Simulate an empty SQL query
    with pytest.raises(OperationalError):
        sql_compiler.execute_sql(result_type=MULTI)