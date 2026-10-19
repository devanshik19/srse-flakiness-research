import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.constants import MULTI, SINGLE, CURSOR, NO_RESULTS

@pytest.fixture
def setup_users():
    User.objects.create(username='user1', password='pass1')
    User.objects.create(username='user2', password='pass2')

def test_execute_sql_multi(setup_users):
    compiler = SQLCompiler(query=User.objects.all().query, connection=connection)
    result = compiler.execute_sql(result_type=MULTI)
    assert len(list(result)) == 2  # Expecting two user entries

def test_execute_sql_single(setup_users):
    compiler = SQLCompiler(query=User.objects.all().query, connection=connection)
    result = compiler.execute_sql(result_type=SINGLE)
    assert result[0] == 'user1'  # Assuming user1 is fetched first

def test_execute_sql_cursor(setup_users):
    compiler = SQLCompiler(query=User.objects.all().query, connection=connection)
    cursor = compiler.execute_sql(result_type=CURSOR)
    rows = list(cursor.fetchall())
    assert len(rows) == 2  # Expecting two user entries

def test_execute_sql_no_results(setup_users):
    compiler = SQLCompiler(query=User.objects.filter(username='non_existent_user').query, connection=connection)
    result = compiler.execute_sql(result_type=NO_RESULTS)
    assert result is None  # No results should return None

def test_execute_sql_empty_result_set():
    compiler = SQLCompiler(query=User.objects.filter(username='another_non_existent_user').query, connection=connection)
    result = compiler.execute_sql(result_type=MULTI)
    assert list(result) == []  # Should return an empty iterator