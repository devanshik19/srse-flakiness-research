import pytest
from django.db import connection
from django.db.models.sql.compiler import SQLCompiler
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_get_combinator_sql_union():
    # Prepare SQLCompiler instance
    query = Query(User)
    compiler = SQLCompiler(query, connection, using='')
    
    # Create a combined query
    query1 = Query(User).filter(is_active=True)
    query2 = Query(User).filter(is_staff=True)
    
    query.combined_queries = [query1, query2]
    
    # Test UNION combinator
    result, params = compiler.get_combinator_sql('union', False)
    assert len(result) > 0
    assert ' UNION ' in result[0]
    
def test_get_combinator_sql_union_all():
    # Prepare SQLCompiler instance
    query = Query(User)
    compiler = SQLCompiler(query, connection, using='')
    
    # Create a combined query
    query1 = Query(User).filter(is_active=True)
    query2 = Query(User).filter(is_staff=True)
    
    query.combined_queries = [query1, query2]
    
    # Test UNION ALL combinator
    result, params = compiler.get_combinator_sql('union', True)
    assert len(result) > 0
    assert ' UNION ALL ' in result[0]

def test_get_combinator_sql_difference():
    # Prepare SQLCompiler instance
    query = Query(User)
    compiler = SQLCompiler(query, connection, using='')
    
    # Create a combined query
    query1 = Query(User).filter(is_active=True)
    query2 = Query(User).filter(is_staff=True)
    
    query.combined_queries = [query1, query2]
    
    # Test DIFFERENCE combinator
    result, params = compiler.get_combinator_sql('difference', False)
    assert len(result) > 0
    assert ' DIFFERENCE ' in result[0]

def test_get_combinator_sql_empty_result():
    # Prepare SQLCompiler instance
    query = Query(User)
    compiler = SQLCompiler(query, connection, using='')
    
    # Create combined queries with no results
    query1 = Query(User).filter(is_active=False)
    query2 = Query(User).filter(is_staff=False)
    
    query.combined_queries = [query1, query2]
    
    # Test handling of EmptyResultSet
    with pytest.raises(EmptyResultSet):
        compiler.get_combinator_sql('union', False)

def test_get_combinator_sql_limit_offset_error():
    # Prepare SQLCompiler instance
    query = Query(User)
    compiler = SQLCompiler(query, connection, using='')
    
    # Create a query with limit and offset which is not allowed
    query1 = Query(User).filter(is_active=True)
    query1.low_mark = 0
    query1.high_mark = 10
    
    query.combined_queries = [query1]
    
    # Test handling of LIMIT/OFFSET error
    with pytest.raises(DatabaseError, match='LIMIT/OFFSET not allowed in subqueries of compound statements.'):
        compiler.get_combinator_sql('union', False)