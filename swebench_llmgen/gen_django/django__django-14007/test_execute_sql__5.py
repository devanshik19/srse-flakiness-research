import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.query import QuerySet
from django.db.models import Query

@pytest.fixture
def active_user():
    user = User.objects.create(username='testuser', password='testpass')
    return user

def test_execute_sql_single_result(active_user):
    compiler = SQLCompiler(Query(User), connection)
    result = compiler.execute_sql(result_type='SINGLE')
    assert result == (active_user.id, active_user.username)  # Adjust based on User fields

def test_execute_sql_multi_results(active_user):
    compiler = SQLCompiler(Query(User), connection)
    result = compiler.execute_sql(result_type='MULTI')
    result_list = list(result)
    assert len(result_list) > 0
    assert all(isinstance(row, tuple) for row in result_list)  # Ensure rows are tuples

def test_execute_sql_empty_result():
    compiler = SQLCompiler(Query(User).filter(username='nonexistentuser'), connection)
    result = compiler.execute_sql(result_type='MULTI')
    assert list(result) == []  # Expecting an empty list for nonexistent users

def test_execute_sql_cursor_return():
    compiler = SQLCompiler(Query(User), connection)
    cursor = compiler.execute_sql(result_type='CURSOR')
    assert cursor is not None
    cursor.close()  # Ensure to close the cursor

def test_execute_sql_no_results():
    compiler = SQLCompiler(Query(User).filter(pk=-1), connection)
    result = compiler.execute_sql(result_type=None)
    assert result is None  # Expecting None for empty set