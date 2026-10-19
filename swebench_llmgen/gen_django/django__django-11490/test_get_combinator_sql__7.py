import pytest
from django.db.models import Q
from django.db import connection
from django.contrib.auth.models import User
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query

def test_get_combinator_sql_union():
    # Prepare two queries that can be combined
    query1 = Query(User.objects.all())
    query2 = Query(User.objects.filter(username='testuser'))

    # Associate the queries with the SQLCompiler
    sql_compiler1 = SQLCompiler(query1, connection, using='default')
    sql_compiler2 = SQLCompiler(query2, connection, using='default')

    # Assign the combined queries
    sql_compiler1.query.combined_queries = [query1, query2]
    
    # Test UNION
    result, params = sql_compiler1.get_combinator_sql('union', all=False)

    # Assert SQL structure and parameters
    assert len(result) == 1
    assert 'UNION' in result[0]
    assert params == []

def test_get_combinator_sql_union_all():
    query1 = Query(User.objects.all())
    query2 = Query(User.objects.filter(username='testuser'))

    sql_compiler1 = SQLCompiler(query1, connection, using='default')
    sql_compiler1.query.combined_queries = [query1, query2]

    # Test UNION ALL
    result, params = sql_compiler1.get_combinator_sql('union', all=True)

    # Assert SQL structure and parameters
    assert len(result) == 1
    assert 'UNION ALL' in result[0]
    assert params == []

def test_get_combinator_sql_difference():
    query1 = Query(User.objects.all())
    query2 = Query(User.objects.filter(username='testuser'))

    sql_compiler1 = SQLCompiler(query1, connection, using='default')
    sql_compiler1.query.combined_queries = [query1, query2]

    # Test DIFFERENCE
    result, params = sql_compiler1.get_combinator_sql('difference', all=False)

    # Assert SQL structure and parameters
    assert len(result) == 1
    assert 'EXCEPT' in result[0]  # Note: difference is represented as EXCEPT
    assert params == []

def test_get_combinator_sql_no_queries():
    query1 = Query(User.objects.none())

    sql_compiler1 = SQLCompiler(query1, connection, using='default')
    sql_compiler1.query.combined_queries = [query1]

    # Test handling of no valid queries
    with pytest.raises(EmptyResultSet):
        sql_compiler1.get_combinator_sql('union', all=False)

def test_get_combinator_sql_with_empty_set():
    query1 = Query(User.objects.filter(username='nonexistent'))
    query2 = Query(User.objects.all())

    sql_compiler1 = SQLCompiler(query1, connection, using='default')
    sql_compiler1.query.combined_queries = [query1, query2]

    # Test handling of empty set in combination
    result, params = sql_compiler1.get_combinator_sql('union', all=False)

    assert len(result) == 1
    assert params == []