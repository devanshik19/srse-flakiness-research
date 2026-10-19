import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.where import WhereNode

def test_as_sql_with_and_connector():
    child1 = Q(username='testuser1')
    child2 = Q(password='testpassword')
    where_node = WhereNode([child1, child2], connector='AND', negated=False)

    sql, params = where_node.as_sql(None, None)

    assert "username = %s" in sql
    assert "password = %s" in sql
    assert params == ['testuser1', 'testpassword']

def test_as_sql_with_or_connector():
    child1 = Q(username='testuser1')
    child2 = Q(password='testpassword')
    where_node = WhereNode([child1, child2], connector='OR', negated=False)

    sql, params = where_node.as_sql(None, None)

    assert "username = %s" in sql
    assert "password = %s" in sql
    assert params == ['testuser1', 'testpassword']

def test_as_sql_empty_node():
    where_node = WhereNode([], connector='AND', negated=False)

    with pytest.raises(EmptyResultSet):
        where_node.as_sql(None, None)

def test_as_sql_full_node():
    child1 = Q(username='testuser1')
    where_node = WhereNode([child1], connector='AND', negated=False)

    sql, params = where_node.as_sql(None, None)

    assert sql == "(username = %s)"
    assert params == ['testuser1']

def test_as_sql_negated_node():
    child1 = Q(username='testuser1')
    where_node = WhereNode([child1], connector='AND', negated=True)

    sql, params = where_node.as_sql(None, None)

    assert sql == "NOT (username = %s)"
    assert params == ['testuser1']

def test_as_sql_with_xor_connector():
    child1 = Q(username='testuser1')
    child2 = Q(password='testpassword')
    where_node = WhereNode([child1, child2], connector='XOR', negated=False)

    with pytest.raises(FullResultSet):
        where_node.as_sql(None, None)