import pytest
from django.db import connection
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.compiler import SQLCompiler

def test_as_sql_with_limits():
    query = User.objects.all()  # A simple query to test
    compiler = SQLCompiler(query, connection)
    sql, params = compiler.as_sql(with_limits=True)

    assert "SELECT" in sql
    assert "FROM" in sql
    assert params == []  # No parameters expected for a simple query

def test_as_sql_without_limits():
    query = User.objects.all()  # A simple query to test
    compiler = SQLCompiler(query, connection)
    sql, params = compiler.as_sql(with_limits=False)

    assert "SELECT" in sql
    assert "FROM" in sql
    assert params == []  # No parameters expected for a simple query

def test_as_sql_with_ordering():
    query = User.objects.all().order_by('username')  # Adding ordering
    compiler = SQLCompiler(query, connection)
    sql, params = compiler.as_sql()

    assert "ORDER BY" in sql
    assert sql.count("ORDER BY") == 1  # Only one order by clause

def test_as_sql_with_group_by():
    query = User.objects.values('username').annotate(count=User.objects.count())
    compiler = SQLCompiler(query, connection)
    sql, params = compiler.as_sql()

    assert "GROUP BY" in sql
    assert sql.count("GROUP BY") == 1  # Ensure group by is included

def test_as_sql_with_empty_results():
    query = User.objects.filter(Q(username='non_existing_user'))  # No results expected
    compiler = SQLCompiler(query, connection)
    
    with pytest.raises(EmptyResultSet):
        sql, params = compiler.as_sql()