import pytest
from django.contrib.auth.models import User
from django.db import connection, DatabaseError
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query

@pytest.fixture
def setup_queries():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    query1 = Query(User)
    query2 = Query(User)

    query1.add_filter(('username', 'user1'))
    query2.add_filter(('username', 'user2'))
    
    return query1, query2

def test_get_combinator_sql_union(setup_queries):
    query1, query2 = setup_queries
    combinator = 'union'
    all = False
    
    compiler1 = query1.get_compiler('default', connection)
    compiler2 = query2.get_compiler('default', connection)
    
    # Manually assigning combined queries to the compiler
    compiler1.query.combined_queries = [query1, query2]
    
    result, params = compiler1.get_combinator_sql(combinator, all)
    
    expected_sql = 'SELECT * FROM ({}) UNION SELECT * FROM ({})'.format(
        *[sql for sql, _ in [(compiler1.as_sql()[0], []), (compiler2.as_sql()[0], [])]]
    )
    assert result[0] == expected_sql
    assert params == []

def test_get_combinator_sql_difference(setup_queries):
    query1, query2 = setup_queries
    combinator = 'difference'
    all = False
    
    compiler1 = query1.get_compiler('default', connection)
    compiler2 = query2.get_compiler('default', connection)

    compiler1.query.combined_queries = [query1, query2]

    with pytest.raises(EmptyResultSet):
        compiler1.get_combinator_sql(combinator, all)

def test_get_combinator_sql_no_queries():
    query = Query(User)
    compiler = query.get_compiler('default', connection)
    compiler.query.combined_queries = []
    
    with pytest.raises(EmptyResultSet):
        compiler.get_combinator_sql('union', False)

def test_get_combinator_sql_with_ordering_error(setup_queries):
    query1, query2 = setup_queries
    query1.add_ordering('username')
    
    combinator = 'union'
    all = False

    compiler1 = query1.get_compiler('default', connection)
    compiler1.query.combined_queries = [query1, query2]

    with pytest.raises(DatabaseError, match='ORDER BY not allowed in subqueries of compound statements.'):
        compiler1.get_combinator_sql(combinator, all)

def test_get_combinator_sql_with_limit_offset_error(setup_queries):
    query1, query2 = setup_queries
    query1.low_mark = 1
    query1.high_mark = 10
    
    combinator = 'union'
    all = False

    compiler1 = query1.get_compiler('default', connection)
    compiler1.query.combined_queries = [query1, query2]

    with pytest.raises(DatabaseError, match='LIMIT/OFFSET not allowed in subqueries of compound statements.'):
        compiler1.get_combinator_sql(combinator, all)