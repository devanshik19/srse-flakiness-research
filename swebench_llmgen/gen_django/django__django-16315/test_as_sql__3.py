import pytest
from django.contrib.auth.models import User
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query
from django.db.backends.base.base import BaseDatabaseWrapper

@pytest.fixture
def sql_compiler():
    query = Query(model=User)
    connection = BaseDatabaseWrapper()  # Use a real connection for tests
    return SQLCompiler(query, connection, using='default', elide_empty=False)

def test_as_sql_with_limits(sql_compiler):
    sql, params = sql_compiler.as_sql(with_limits=True)
    assert "SELECT" in sql
    assert sql.startswith("SELECT")
    assert isinstance(params, tuple)

def test_as_sql_without_limits(sql_compiler):
    sql, params = sql_compiler.as_sql(with_limits=False)
    assert "SELECT" in sql
    assert sql.startswith("SELECT")
    assert isinstance(params, tuple)

def test_as_sql_with_order_by(sql_compiler):
    sql_compiler.query.order_by = ['username']
    sql, params = sql_compiler.as_sql()
    assert "ORDER BY" in sql

def test_as_sql_with_group_by(sql_compiler):
    sql_compiler.query.group_by = ['email']
    sql, params = sql_compiler.as_sql()
    assert "GROUP BY" in sql

def test_as_sql_with_select_for_update(sql_compiler):
    sql_compiler.query.select_for_update = True
    sql, params = sql_compiler.as_sql()
    assert "SELECT FOR UPDATE" in sql

def test_as_sql_empty_result_set(sql_compiler):
    sql_compiler.where = None  # Assuming there are no conditions
    with pytest.raises(Exception) as excinfo:
        sql_compiler.as_sql()
    assert '0 = 1' in str(excinfo.value)

def test_as_sql_full_result_set(sql_compiler):
    sql_compiler.query.select_for_update = True
    sql_compiler.where = None  # Assuming there are no conditions
    sql_compiler.having = None
    sql, params = sql_compiler.as_sql()
    assert sql.startswith("SELECT")  # Must return valid SQL even without where or having