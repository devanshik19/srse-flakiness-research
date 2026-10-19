import operator
from functools import reduce
from django.core.exceptions import EmptyResultSet, FullResultSet
from django.db.models.expressions import Case, When
from django.db.models.lookups import Exact
from django.utils import tree
from django.utils.functional import cached_property
import pytest
from django.contrib.auth.models import User
from django.db.models.sql.where import WhereNode

def test_as_sql_with_empty_node():
    where_node = WhereNode(children=[], connector=operator.and_)
    with pytest.raises(EmptyResultSet):
        where_node.as_sql(None, None)

def test_as_sql_with_full_node():
    user_node = WhereNode(children=[User.objects.filter(username='test_user')], connector=operator.and_)
    User.objects.create(username='test_user')
    sql, params = user_node.as_sql(None, None)
    assert sql is not None
    assert params == []

def test_as_sql_with_negated_full_node():
    where_node = WhereNode(children=[User.objects.filter(username='nonexistent_user')], connector=operator.and_)
    with pytest.raises(FullResultSet):
        where_node.as_sql(None, None)

def test_as_sql_with_component_nodes():
    existing_user = User.objects.create(username='test_user_1')
    where_node = WhereNode(children=[
        WhereNode(children=[User.objects.filter(username='test_user_1')], connector=operator.and_),
        WhereNode(children=[User.objects.filter(username='test_user_2')], connector=operator.and_)
    ], connector=operator.or_)
    
    sql, params = where_node.as_sql(None, None)
    assert 'SELECT' in sql  # Assuming that we have a valid sql command
    assert 'test_user_1' in sql
    assert params == []

def test_as_sql_with_xor_logic():
    where_node = WhereNode(children=[
        User.objects.filter(username='test_user_1'), 
        User.objects.filter(username='test_user_2')
    ], connector=operator.xor)

    with pytest.raises(EmptyResultSet):
        where_node.as_sql(None, None)

def test_as_sql_without_any_children():
    where_node = WhereNode(children=[], connector=operator.or_)
    with pytest.raises(EmptyResultSet):
        where_node.as_sql(None, None)

def test_as_sql_with_combined_conditions():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    where_node = WhereNode(children=[
        WhereNode(children=[User.objects.filter(username='user1')], connector=operator.and_),
        WhereNode(children=[User.objects.filter(username='user2')], connector=operator.and_)
    ], connector=operator.and_)

    sql, params = where_node.as_sql(None, None)
    assert 'user1' in sql or 'user2' in sql
    assert params == []