import pytest
from django.db import connections
from django.db.models.sql.compiler import SQLCompiler
from django.contrib.auth.models import User
from django.db.models import QuerySet

@pytest.fixture
def user_queryset():
    """Fixture to create a user queryset."""
    User.objects.create(username='user1')
    User.objects.create(username='user2')
    return User.objects.all()

def test_as_sql_with_limits(user_queryset):
    compiler = SQLCompiler(user_queryset.query, connections['default'], using='default')
    sql, params = compiler.as_sql(with_limits=True)
    assert "SELECT" in sql
    assert "FROM" in sql
    assert len(params) == 0  # No parameters for simple SELECT

def test_as_sql_without_limits(user_queryset):
    compiler = SQLCompiler(user_queryset.query, connections['default'], using='default')
    sql, params = compiler.as_sql(with_limits=False)
    assert "SELECT" in sql
    assert "FROM" in sql
    assert "LIMIT" not in sql
    assert "OFFSET" not in sql
    assert len(params) == 0  # No parameters for simple SELECT

def test_as_sql_with_distinct(user_queryset):
    user_queryset = user_queryset.distinct()
    compiler = SQLCompiler(user_queryset.query, connections['default'], using='default')
    sql, params = compiler.as_sql()
    assert "SELECT DISTINCT" in sql

def test_as_sql_with_ordering(user_queryset):
    user_queryset = user_queryset.order_by('username')
    compiler = SQLCompiler(user_queryset.query, connections['default'], using='default')
    sql, params = compiler.as_sql()
    assert "ORDER BY" in sql

def test_as_sql_with_invalid_combinator():
    """Test for handling of an unsupported combinator."""
    from django.db.models.sql.query import Query
    query = Query()
    query.combinator = "INTERSECT"  # Assume the backend doesn't support this
    compiler = SQLCompiler(query, connections['default'], using='default')

    with pytest.raises(NotSupportedError):
        compiler.as_sql(with_limits=True)

def test_as_sql_with_group_by(user_queryset):
    user_queryset = user_queryset.values('username').annotate(count=models.Count('id'))
    compiler = SQLCompiler(user_queryset.query, connections['default'], using='default')
    sql, params = compiler.as_sql()
    assert "GROUP BY" in sql