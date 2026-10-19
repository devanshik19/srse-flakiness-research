import pytest
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query
from django.db import connection
from django.contrib.auth.models import User

@pytest.mark.parametrize("with_limits, with_col_aliases", [
    (True, False),
    (False, True),
])
def test_as_sql_with_limits_and_col_aliases(with_limits, with_col_aliases):
    # Create a simple query
    query = Query(User)
    query.add_fields(['username', 'email'], None)
    query.set_select(['username', 'email'])
    
    # Prepare the SQL compiler
    compiler = SQLCompiler(query, connection)

    sql, params = compiler.as_sql(with_limits=with_limits, with_col_aliases=with_col_aliases)

    # Basic assertions
    assert isinstance(sql, str)
    assert isinstance(params, tuple)
    assert "SELECT" in sql
    assert "FROM" in sql

    if with_limits:
        assert "LIMIT" in sql or "OFFSET" in sql
        
    # Check if the selected columns are present in the SQL
    for field in ['username', 'email']:
        assert field in sql

@pytest.mark.parametrize("distinct_enabled", [True, False])
def test_as_sql_with_distinct(distinct_enabled):
    # Create a simple query with distinct
    query = Query(User)
    query.add_fields(['username', 'email'], None)
    if distinct_enabled:
        query.distinct = True
    query.set_select(['username', 'email'])
    
    # Prepare the SQL compiler
    compiler = SQLCompiler(query, connection)

    sql, params = compiler.as_sql(with_limits=False, with_col_aliases=False)

    # Basic assertions
    assert isinstance(sql, str)
    assert isinstance(params, tuple)
    assert "SELECT" in sql
    assert "FROM" in sql
    
    if distinct_enabled:
        assert "DISTINCT" in sql
    else:
        assert "DISTINCT" not in sql

def test_as_sql_empty_result_set():
    # Create a query that results in an EmptyResultSet
    query = Query(User)
    query.add_fields(['username', 'email'], None)
    query.set_select(['username', 'email'])
    query.where = []  # No conditions
    
    # Prepare the SQL compiler
    compiler = SQLCompiler(query, connection)

    with pytest.raises(EmptyResultSet):
        compiler.as_sql(with_limits=True, with_col_aliases=False)

def test_as_sql_full_result_set():
    # Create a query that results in a FullResultSet
    query = Query(User)
    query.add_fields(['username'], None)
    query.set_select(['username'])
    
    # Prepare the SQL compiler
    compiler = SQLCompiler(query, connection)

    sql, params = compiler.as_sql(with_limits=False, with_col_aliases=False)

    assert isinstance(sql, str)
    assert isinstance(params, tuple)
    assert "SELECT" in sql
    assert "FROM" in sql