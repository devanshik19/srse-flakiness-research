import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.constants import MULTI, SINGLE, CURSOR, NO_RESULTS

def test_execute_sql_multi():
    user = User.objects.create_user(username='testuser', password='testpass')
    compiler = SQLCompiler()

    # Simulate as_sql() return values
    def mock_as_sql():
        return ("SELECT * FROM auth_user WHERE username = %s", [user.username])
    
    compiler.as_sql = mock_as_sql
    results = compiler.execute_sql(result_type=MULTI)
    
    assert list(results) == [(user.id, user.username, user.password, user.last_login, user.is_superuser,
                               user.is_staff, user.is_active, user.date_joined)]

def test_execute_sql_single():
    user = User.objects.create_user(username='testuser', password='testpass')
    compiler = SQLCompiler()

    # Simulate as_sql() return values
    def mock_as_sql():
        return ("SELECT * FROM auth_user WHERE username = %s", [user.username])

    compiler.as_sql = mock_as_sql
    result = compiler.execute_sql(result_type=SINGLE)

    assert result == (user.id, user.username, user.password, user.last_login, user.is_superuser,
                      user.is_staff, user.is_active, user.date_joined)

def test_execute_sql_no_results():
    compiler = SQLCompiler()

    def mock_as_sql():
        return ("", [])
    
    compiler.as_sql = mock_as_sql
    result = compiler.execute_sql(result_type=NO_RESULTS)

    assert result is None

def test_execute_sql_cursor():
    user = User.objects.create_user(username='testuser', password='testpass')
    compiler = SQLCompiler()

    # Simulate as_sql() return values
    def mock_as_sql():
        return ("SELECT * FROM auth_user WHERE username = %s", [user.username])

    compiler.as_sql = mock_as_sql
    cursor = compiler.execute_sql(result_type=CURSOR)

    fetched = cursor.fetchone()
    assert fetched == (user.id, user.username, user.password, user.last_login, user.is_superuser,
                       user.is_staff, user.is_active, user.date_joined)
    cursor.close()