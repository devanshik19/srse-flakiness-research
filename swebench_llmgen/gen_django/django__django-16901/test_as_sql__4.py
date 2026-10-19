import operator
from functools import reduce
from django.core.exceptions import EmptyResultSet, FullResultSet
from django.db.models.expressions import Case, When
from django.db.models.lookups import Exact
from django.utils import tree
from django.utils.functional import cached_property
from django.db.models.sql.where import WhereNode
from django.contrib.auth.models import User

def test_as_sql_and_connector():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    where_node = WhereNode([Exact('username', 'user1'), Exact('username', 'user2')], connector=operator.and_)
    sql, params = where_node.as_sql(None, None)

    assert sql == "('user1' = username) AND ('user2' = username)"
    assert params == []

def test_as_sql_or_connector():
    where_node = WhereNode([Exact('username', 'user1'), Exact('username', 'user2')], connector=operator.or_)
    sql, params = where_node.as_sql(None, None)

    assert sql == "('user1' = username) OR ('user2' = username)"
    assert params == []

def test_as_sql_xor_connector():
    where_node = WhereNode([Exact('username', 'user1'), Exact('username', 'user2')], connector='XOR')
    
    with pytest.raises(EmptyResultSet):
        where_node.as_sql(None, None)

def test_as_sql_empty_node():
    where_node = WhereNode([], connector=operator.and_)

    with pytest.raises(EmptyResultSet):
        where_node.as_sql(None, None)

def test_as_sql_full_node():
    where_node = WhereNode([Exact('username', 'nonexistent')], connector=operator.and_)
    
    with pytest.raises(FullResultSet):
        where_node.as_sql(None, None)

def test_as_sql_negated_case():
    where_node = WhereNode([Exact('username', 'user1')], connector=operator.and_, negated=True)
    
    sql, params = where_node.as_sql(None, None)
    
    assert sql == "NOT ('user1' = username)"
    assert params == []