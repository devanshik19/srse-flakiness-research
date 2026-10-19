import pytest
from django.db import connection
from django.contrib.auth.models import User
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.constants import MULTI, SINGLE, NO_RESULTS, CURSOR

@pytest.mark.django_db
def test_execute_sql_multi():
    user = User.objects.create(username='testuser')
    compiler = SQLCompiler(query=None, connection=connection)  # query must be a valid Query object
    # Using the actual User.objects.get_queryset() as query instead of None
    from django.db.models import QuerySet
    compiler.query = User.objects.all().query
    result = compiler.execute_sql(MULTI)
    assert isinstance(result, list)
    assert len(result) > 0
    assert user.id in [u.id for u in result]

@pytest.mark.django_db
def test_execute_sql_single():
    user = User.objects.create(username='singleuser')
    compiler = SQLCompiler(query=None, connection=connection)
    compiler.query = User.objects.filter(username='singleuser').query
    result = compiler.execute_sql(SINGLE)
    assert result is not None
    assert result[0] == user.id

@pytest.mark.django_db
def test_execute_sql_no_results():
    compiler = SQLCompiler(query=None, connection=connection)
    compiler.query = User.objects.filter(username='nonexistentuser').query
    result = compiler.execute_sql(NO_RESULTS)
    assert result is None

@pytest.mark.django_db
def test_execute_sql_cursor():
    user = User.objects.create(username='cursoruser')
    compiler = SQLCompiler(query=None, connection=connection)
    compiler.query = User.objects.filter(username='cursoruser').query
    cursor = compiler.execute_sql(CURSOR)
    assert cursor is not None
    assert cursor.fetchone() is not None
    cursor.close()

@pytest.mark.django_db
def test_execute_sql_empty_sql():
    compiler = SQLCompiler(query=None, connection=connection)
    compiler.query = User.objects.none().query  # this produces empty SQL
    result = compiler.execute_sql(MULTI)
    assert isinstance(result, list)
    assert len(result) == 0