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

def test_as_sql_full_resultset():
    user = User.objects.create(username='testuser')
    node = WhereNode()
    node.children = [Case(When(username='testuser', then=1), default=0)]
    node.connector = WhereNode.AND
    node.negated = False
    
    sql, params = node.as_sql(None, None)
    
    assert sql == "(username = testuser)"
    assert params == []

def test_as_sql_empty_resultset():
    node = WhereNode()
    node.children = [Case(When(username='nonexistentuser', then=1), default=0)]
    node.connector = WhereNode.AND
    node.negated = False

    with pytest.raises(EmptyResultSet):
        node.as_sql(None, None)

def test_as_sql_negated_full_resultset():
    node = WhereNode()
    node.children = [Case(When(username='testuser', then=1), default=0)]
    node.connector = WhereNode.AND
    node.negated = True
    
    with pytest.raises(FullResultSet):
        node.as_sql(None, None)

def test_as_sql_multiple_conditions():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    node = WhereNode()
    node.children = [Case(When(username='user1', then=1), When(username='user2', then=1), default=0)]
    node.connector = WhereNode.AND
    node.negated = False
    
    sql, params = node.as_sql(None, None)
    
    assert sql == "(username = user1 OR username = user2)"
    assert params == []

def test_as_sql_xor_condition():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    node = WhereNode()
    node.children = [
        Case(When(username='user1', then=1), default=0),
        Case(When(username='user2', then=1), default=0),
    ]
    node.connector = WhereNode.XOR
    node.negated = False
    
    sql, params = node.as_sql(None, None)
    
    assert sql.startswith("(") and sql.endswith(")")
    assert 'OR' in sql
    assert params == []