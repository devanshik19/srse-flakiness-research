import pytest
from django.contrib.auth.models import User
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query

@pytest.fixture
def query():
    return Query(User)

@pytest.fixture
def sql_compiler(query):
    return SQLCompiler(query, None, None)

def test_get_order_by_with_extra_order_by(sql_compiler):
    sql_compiler.query.extra_order_by = ['username']
    result = sql_compiler.get_order_by()
    assert len(result) == 1
    assert result[0][0].expression == 'username'

def test_get_order_by_without_ordering(sql_compiler):
    sql_compiler.query.extra_order_by = []
    sql_compiler.query.default_ordering = False
    sql_compiler.query.order_by = []
    sql_compiler.query.get_meta().ordering = []
    result = sql_compiler.get_order_by()
    assert result == []

def test_get_order_by_with_default_ordering(sql_compiler):
    sql_compiler.query.default_ordering = True
    sql_compiler.query.order_by = ['-id']
    result = sql_compiler.get_order_by()
    assert len(result) == 1
    assert result[0][0].expression == 'id'
    assert result[0][0].descending is True

def test_get_order_by_with_annotation(sql_compiler):
    sql_compiler.query.annotations = {'age': 25}
    sql_compiler.query.order_by = ['age']
    result = sql_compiler.get_order_by()
    assert len(result) == 1
    assert result[0][0].expression == 25

def test_get_order_by_with_random(sql_compiler):
    sql_compiler.query.order_by = ['?']
    result = sql_compiler.get_order_by()
    assert len(result) == 1
    assert isinstance(result[0][0], SQLCompiler.OrderBy)
    
def test_get_order_by_with_complex_field(sql_compiler):
    sql_compiler.query.order_by = ['email']
    result = sql_compiler.get_order_by()
    assert len(result) == 1
    assert result[0][0].expression == 'email'