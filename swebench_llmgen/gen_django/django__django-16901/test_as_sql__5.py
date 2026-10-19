import operator
from functools import reduce
from django.core.exceptions import EmptyResultSet, FullResultSet
from django.db.models.expressions import Case, When
from django.db.models.lookups import Exact
from django.contrib.auth.models import User
from django.db.models.sql.where import WhereNode

def test_where_node_as_sql_with_empty_node():
    node = WhereNode(children=[], connector="AND", negated=False)
    with pytest.raises(EmptyResultSet):
        node.as_sql(None, None)

def test_where_node_as_sql_with_full_node():
    user = User.objects.create(username='testuser')
    node = WhereNode(children=[user], connector="AND", negated=False)
    sql, params = node.as_sql(None, None)
    assert sql == "(<your SQL representation>)"  # Replace with expected SQL
    assert params == []  # Adjust according to expected params

def test_where_node_as_sql_with_full_negated():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    node = WhereNode(children=[user1, user2], connector="OR", negated=True)
    sql, params = node.as_sql(None, None)
    assert sql == "NOT ((<your SQL representation>))"  # Replace with expected SQL
    assert params == []  # Adjust according to expected params

def test_where_node_as_sql_with_xor_not_supported():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    node = WhereNode(children=[user1, user2], connector="XOR", negated=False)
    with pytest.raises(EmptyResultSet):
        node.as_sql(None, None)

def test_where_node_as_sql_with_children_and_connector():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    node = WhereNode(children=[user1, user2], connector="AND", negated=False)
    sql, params = node.as_sql(None, None)
    assert sql == "(<your SQL representation>)"  # Replace with expected SQL
    assert params == []  # Adjust according to expected params