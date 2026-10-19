import pytest
from django.contrib.auth.models import User
from django.db.models.sql.compiler import SQLCompiler
from django.db import connection, DatabaseError, EmptyResultSet

@pytest.fixture
def sql_compiler():
    query = User.objects.all().query
    return SQLCompiler(query, connection, using=None)

def test_get_combinator_sql_union(sql_compiler):
    # Create two combined queries
    query1 = User.objects.filter(username='testuser1').query
    query2 = User.objects.filter(username='testuser2').query
    sql_compiler.query.set_combined_queries([query1, query2])

    result, params = sql_compiler.get_combinator_sql('union', False)

    assert ' UNION ' in result[0]
    assert params == []

def test_get_combinator_sql_union_all(sql_compiler):
    # Create two combined queries
    query1 = User.objects.filter(username='testuser1').query
    query2 = User.objects.filter(username='testuser2').query
    sql_compiler.query.set_combined_queries([query1, query2])

    result, params = sql_compiler.get_combinator_sql('union', True)

    assert ' UNION ALL ' in result[0]
    assert params == []

def test_get_combinator_sql_difference(sql_compiler):
    # Create two combined queries
    query1 = User.objects.filter(username='testuser1').query
    query2 = User.objects.filter(username='testuser2').query
    sql_compiler.query.set_combined_queries([query1, query2])

    result, params = sql_compiler.get_combinator_sql('difference', False)

    assert ' DIFFERENCE ' in result[0]
    assert params == []

def test_get_combinator_sql_empty_result_set(sql_compiler):
    # Create a combined query with no results
    query1 = User.objects.none().query
    sql_compiler.query.set_combined_queries([query1])

    with pytest.raises(EmptyResultSet):
        sql_compiler.get_combinator_sql('union', False)

def test_get_combinator_sql_limit_not_allowed(sql_compiler):
    # Setup mock for the features to not support slicing
    sql_compiler.connection.features.supports_slicing_ordering_in_compound = False
    
    query1 = User.objects.all().query
    query2 = User.objects.filter(username='testuser2').query
    sql_compiler.query.set_combined_queries([query1, query2])
    sql_compiler.query.low_mark = 1  # Set a LIMIT

    with pytest.raises(DatabaseError, match='LIMIT/OFFSET not allowed in subqueries of compound statements.'):
        sql_compiler.get_combinator_sql('union', False)