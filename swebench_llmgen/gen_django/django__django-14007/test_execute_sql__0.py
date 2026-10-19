import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.constants import MULTI, SINGLE, CURSOR, NO_RESULTS

def test_execute_sql_empty_result():
    query = User.objects.filter(username='nonexistent_user')
    compiler = SQLCompiler(query.query, connection)
    
    result = compiler.execute_sql(result_type=MULTI)
    assert list(result) == []

def test_execute_sql_single_result():
    user = User.objects.create(username='testuser', password='password')
    query = User.objects.filter(username='testuser')
    compiler = SQLCompiler(query.query, connection)

    result = compiler.execute_sql(result_type=SINGLE)
    assert result == (user.id, user.username, user.password)

def test_execute_sql_cursor_result():
    user = User.objects.create(username='cursoruser', password='password')
    query = User.objects.filter(username='cursoruser')
    compiler = SQLCompiler(query.query, connection)

    cursor = compiler.execute_sql(result_type=CURSOR)
    row = cursor.fetchone()
    assert row == (user.id, user.username, user.password)
    cursor.close()

def test_execute_sql_no_results_with_empty_set():
    query = User.objects.filter(username='another_nonexistent_user')
    compiler = SQLCompiler(query.query, connection)

    result = compiler.execute_sql(result_type=NO_RESULTS)
    assert result is None

def test_execute_sql_chunked_fetch():
    user_1 = User.objects.create(username='chunkuser1', password='password')
    user_2 = User.objects.create(username='chunkuser2', password='password')
    
    query = User.objects.all()
    compiler = SQLCompiler(query.query, connection)

    result = compiler.execute_sql(result_type=MULTI, chunked_fetch=True)
    assert list(result) == [(user_1.id, user_1.username, user_1.password), (user_2.id, user_2.username, user_2.password)]