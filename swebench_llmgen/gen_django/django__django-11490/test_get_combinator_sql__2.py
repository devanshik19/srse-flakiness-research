import pytest
from django.contrib.auth.models import User
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query
from django.db.utils import DatabaseError, EmptyResultSet

@pytest.fixture
def sql_compiler():
    query = Query(model=User)
    connection = query.get_queryer()
    return SQLCompiler(query, connection, using='default')

def test_get_combinator_sql_union(sql_compiler):
    user_query1 = User.objects.filter(username='user1')
    user_query2 = User.objects.filter(username='user2')
    sql_compiler.query.combined_queries = [user_query1.query, user_query2.query]

    result_sql, result_params = sql_compiler.get_combinator_sql('union', all=False)

    assert 'UNION' in result_sql[0]
    assert len(result_params) == 0  # No parameters for basic case

def test_get_combinator_sql_union_all(sql_compiler):
    user_query1 = User.objects.filter(username='user1')
    user_query2 = User.objects.filter(username='user2')
    sql_compiler.query.combined_queries = [user_query1.query, user_query2.query]

    result_sql, result_params = sql_compiler.get_combinator_sql('union', all=True)

    assert 'UNION ALL' in result_sql[0]
    assert len(result_params) == 0  # No parameters for basic case

def test_get_combinator_sql_difference(sql_compiler):
    user_query1 = User.objects.filter(username='user1')
    user_query2 = User.objects.filter(username='user2')
    sql_compiler.query.combined_queries = [user_query1.query, user_query2.query]

    result_sql, result_params = sql_compiler.get_combinator_sql('difference', all=False)

    assert 'DIFFERENCE' in result_sql[0]
    assert len(result_params) == 0  # No parameters for basic case

def test_get_combinator_sql_empty_result_set(sql_compiler):
    user_query1 = User.objects.none()  # This results in an empty queryset
    user_query2 = User.objects.filter(username='user2')
    sql_compiler.query.combined_queries = [user_query1.query, user_query2.query]

    with pytest.raises(EmptyResultSet):
        sql_compiler.get_combinator_sql('union', all=False)

def test_get_combinator_sql_invalid_subquery(sql_compiler):
    user_query1 = User.objects.filter(username='user1').order_by('date_joined')
    user_query2 = User.objects.filter(username='user2')
    sql_compiler.query.combined_queries = [user_query1.query, user_query2.query]

    with pytest.raises(DatabaseError, match='ORDER BY not allowed in subqueries of compound statements.'):
        sql_compiler.get_combinator_sql('union', all=False)