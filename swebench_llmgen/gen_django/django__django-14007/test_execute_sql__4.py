import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.constants import MULTI, SINGLE, CURSOR, NO_RESULTS

@pytest.fixture
def setup_user():
    User.objects.create(username='testuser', password='password123')
    yield
    User.objects.filter(username='testuser').delete()

def test_execute_sql_multi(setup_user):
    compiler = SQLCompiler(query=None, connection=connection, using=None)
    result = compiler.execute_sql(result_type=MULTI)
    assert isinstance(result, list)
    assert len(result) > 0

def test_execute_sql_single(setup_user):
    compiler = SQLCompiler(query=None, connection=connection, using=None)
    result = compiler.execute_sql(result_type=SINGLE)
    assert result is not None

def test_execute_sql_cursor(setup_user):
    compiler = SQLCompiler(query=None, connection=connection, using=None)
    cursor = compiler.execute_sql(result_type=CURSOR)
    assert cursor is not None
    assert isinstance(cursor, connection.cursor().__class__)
    cursor.close()

def test_execute_sql_no_results_empty(setup_user):
    compiler = SQLCompiler(query=None, connection=connection, using=None)
    result = compiler.execute_sql(result_type=NO_RESULTS)
    assert result is None

def test_execute_sql_empty_result_set(setup_user):
    class EmptyQuery(SQLCompiler):
        def as_sql(self):
            return "", []

    compiler = EmptyQuery(query=None, connection=connection, using=None)

    result = compiler.execute_sql(result_type=MULTI)
    assert result == []

    result = compiler.execute_sql(result_type=SINGLE)
    assert result is None

    cursor = compiler.execute_sql(result_type=CURSOR)
    assert cursor is None