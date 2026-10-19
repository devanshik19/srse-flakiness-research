import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.models import F
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query

@pytest.fixture
def sql_compiler():
    query = Query(User)
    return SQLCompiler(query, connection, using='default')

def test_find_ordering_name_asc(sql_compiler):
    opts = User._meta
    name = 'username'
    expected = sql_compiler.find_ordering_name(name, opts)
    assert len(expected) == 1
    assert expected[0][0].expression.name == 'username'
    assert expected[0][1] is False

def test_find_ordering_name_desc(sql_compiler):
    opts = User._meta
    name = 'username__desc'
    expected = sql_compiler.find_ordering_name(name, opts, default_order='DESC')
    assert len(expected) == 1
    assert expected[0][0].expression.name == 'username'
    assert expected[0][1] is True

def test_find_ordering_name_multiple_levels(sql_compiler):
    opts = User._meta
    name = 'profile__bio'
    with pytest.raises(FieldError):
        sql_compiler.find_ordering_name(name, opts)

def test_find_ordering_name_infinite_loop(sql_compiler):
    opts = User._meta
    name = 'username'
    sql_compiler.query.alias_map = {1: type('Alias', (), {'join_cols': (1,)})}  # Constructing a mock alias
    sql_compiler.query.joined_tables = ('table1', 'table2')
    sql_compiler.query.alias_map = {1: sql_compiler.query.alias_map[1]}
    sql_compiler.query.processed_joins = (1, 1)  # Simulate already seen joins
    with pytest.raises(FieldError, match='Infinite loop caused by ordering'):
        sql_compiler.find_ordering_name(name, opts)