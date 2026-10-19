import pytest
from django.db import connection
from django.db.models.sql.compiler import SQLCompiler
from django.contrib.auth.models import User

@pytest.fixture
def sql_compiler():
    # Create a mock query and connection for SQLCompiler
    query = User.objects.all().query
    return SQLCompiler(query, connection)

def test_execute_sql_single(sql_compiler):
    # Test SINGLE result_type
    result = sql_compiler.execute_sql(result_type='SINGLE')
    assert isinstance(result, User)  # Assuming a user exists in the test database
    assert result is not None

def test_execute_sql_multi(sql_compiler):
    # Test MULTI result_type
    results = sql_compiler.execute_sql(result_type='MULTI')
    user_list = list(results)
    assert len(user_list) > 0  # Assuming there is at least one user
    assert all(isinstance(user, User) for user in user_list)

def test_execute_sql_no_results(sql_compiler):
    # Modify the query to ensure no results returned
    sql_compiler.query = User.objects.filter(id=-1).query
    result = sql_compiler.execute_sql(result_type='MULTI')
    assert list(result) == []

def test_execute_sql_cursor(sql_compiler):
    # Test CURSOR result_type
    cursor = sql_compiler.execute_sql(result_type='CURSOR')
    assert cursor is not None
    data = cursor.fetchall()
    cursor.close()
    assert all(isinstance(row, tuple) for row in data)

def test_execute_sql_empty_result_set(sql_compiler):
    # Modify the query to ensure an EmptyResultSet exception is raised
    sql_compiler.query = User.objects.filter(id=-1).query
    with pytest.raises(Exception) as excinfo:
        sql_compiler.execute_sql(result_type='SINGLE')
    assert 'EmptyResultSet' in str(excinfo.value)