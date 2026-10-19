import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.constants import MULTI, SINGLE, NO_RESULTS, CURSOR

@pytest.fixture
def user():
    return User.objects.create(username='testuser', password='testpassword')

def test_execute_sql_multi(user):
    compiler = SQLCompiler(None, connection)
    result = compiler.execute_sql(result_type=MULTI)
    assert isinstance(result, list)

def test_execute_sql_single(user):
    compiler = SQLCompiler(None, connection)
    result = compiler.execute_sql(result_type=SINGLE)
    assert result is not None
    assert isinstance(result, tuple)

def test_execute_sql_no_results(user):
    compiler = SQLCompiler(None, connection)
    result = compiler.execute_sql(result_type=NO_RESULTS)
    assert result is None

def test_execute_sql_empty_sql():
    compiler = SQLCompiler(None, connection)
    compiler.as_sql = lambda: ('', [])
    with pytest.raises(EmptyResultSet):
        compiler.execute_sql(result_type=MULTI)

def test_execute_sql_cursor(user):
    compiler = SQLCompiler(None, connection)
    result = compiler.execute_sql(result_type=CURSOR)
    assert result is not None
    assert hasattr(result, 'close')

def test_execute_sql_chunked_fetch(user):
    compiler = SQLCompiler(None, connection)
    result = compiler.execute_sql(chunked_fetch=True)
    assert isinstance(result, list) or hasattr(result, '__iter__')