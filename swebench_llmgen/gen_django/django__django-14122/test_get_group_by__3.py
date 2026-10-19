import collections
import re
from functools import partial
from itertools import chain
from django.contrib.auth.models import User
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query
import pytest

@pytest.fixture
def sql_compiler():
    query = Query(User)
    return SQLCompiler(query, None, None)

def test_get_group_by_no_group_by(sql_compiler):
    sql_compiler.query.group_by = None
    assert sql_compiler.get_group_by([], []) == []

def test_get_group_by_group_by_true(sql_compiler):
    sql_compiler.query.group_by = True
    assert sql_compiler.get_group_by([], []) != []

def test_get_group_by_with_values(sql_compiler):
    sql_compiler.query.group_by = ['username']
    select = [(User.objects.values('username'), None, False)]
    order_by = []
    result = sql_compiler.get_group_by(select, order_by)
    assert len(result) == 1
    assert result[0][0] == 'username'

def test_get_group_by_with_multiple_selects(sql_compiler):
    sql_compiler.query.group_by = ['username', 'email']
    select = [(User.objects.values('username', 'email'), None, False)]
    order_by = []
    result = sql_compiler.get_group_by(select, order_by)
    assert len(result) == 2
    assert set((r[0] for r in result)) == {'username', 'email'}

def test_get_group_by_with_order_by(sql_compiler):
    sql_compiler.query.group_by = ['username']
    select = [(User.objects.values('username'), None, False)]
    order_by = [(User.objects.order_by('username'), ('username', []), True)]
    
    result = sql_compiler.get_group_by(select, order_by)
    assert len(result) == 1
    assert result[0][0] == 'username'

def test_get_group_by_with_having(sql_compiler):
    sql_compiler.query.group_by = ['username']
    sql_compiler.having = collections.namedtuple('Having', ['get_group_by_cols'])(lambda: ['username', 'email'])
    
    select = [(User.objects.values('username'), None, False)]
    order_by = []
    result = sql_compiler.get_group_by(select, order_by)
    
    assert len(result) == 2
    assert set((r[0] for r in result)) == {'username', 'email'}