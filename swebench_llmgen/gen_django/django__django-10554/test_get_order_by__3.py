import pytest
from django.db.models.sql.compiler import SQLCompiler
from django.db.models import QuerySet
from django.contrib.auth.models import User
from django.db.models.expressions import OrderBy, Value
from django.db.models.functions import Cast

@pytest.fixture
def query_set():
    return User.objects.all()

def test_get_order_by_no_ordering(query_set):
    compiler = SQLCompiler(query=query_set.query, connection=query_set.db)
    result = compiler.get_order_by()
    assert result == []

def test_get_order_by_with_extra_order_by(query_set):
    query_set = query_set.extra(order_by=['username'])
    compiler = SQLCompiler(query=query_set.query, connection=query_set.db)
    result = compiler.get_order_by()
    
    assert len(result) == 1
    assert result[0][0].expression == 'username'

def test_get_order_by_with_default_ordering(query_set):
    query_set = query_set.order_by('date_joined')
    compiler = SQLCompiler(query=query_set.query, connection=query_set.db)
    result = compiler.get_order_by()
    
    assert len(result) == 1
    assert result[0][0].expression == 'date_joined'

def test_get_order_by_with_annotations(query_set):
    from django.db.models import Count

    query_set = query_set.annotate(num_posts=Count('post'))
    query_set = query_set.order_by('num_posts')
    compiler = SQLCompiler(query=query_set.query, connection=query_set.db)
    result = compiler.get_order_by()
    
    assert len(result) == 1
    assert result[0][0].expression == 'num_posts'

def test_get_order_by_with_reverse_ordering(query_set):
    query_set = query_set.order_by('-date_joined')
    compiler = SQLCompiler(query=query_set.query, connection=query_set.db)
    result = compiler.get_order_by()

    assert len(result) == 1
    assert result[0][0].expression == 'date_joined'
    assert result[0][0].descending is True

def test_get_order_by_with_random(query_set):
    query_set = query_set.order_by('?')
    compiler = SQLCompiler(query=query_set.query, connection=query_set.db)
    result = compiler.get_order_by()
    
    assert len(result) == 1
    assert isinstance(result[0][0], OrderBy)
    assert result[0][0].expression.__class__.__name__ == 'Random'