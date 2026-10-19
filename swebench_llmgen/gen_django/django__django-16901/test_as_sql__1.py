import operator
from functools import reduce
from django.core.exceptions import EmptyResultSet, FullResultSet
from django.db.models.expressions import Case, When
from django.db.models.lookups import Exact
from django.contrib.auth.models import User
from django.db.models.sql.where import WhereNode
from django.db.models.sql import AND, OR

def test_as_sql_with_full_result():
    user = User.objects.create(username='testuser')
    node = WhereNode([User._meta.get_field('username').exact('testuser')], AND)
    
    sql, params = node.as_sql(None, None)
    
    assert sql == "(username = %s)"
    assert params == ['testuser']

def test_as_sql_with_empty_result():
    node = WhereNode([User._meta.get_field('username').exact('nonexistent_user')], AND)
    
    with pytest.raises(EmptyResultSet):
        node.as_sql(None, None)

def test_as_sql_with_full_needed_and_empty_needed():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    node = WhereNode([
        User._meta.get_field('username').exact('user1'),
        User._meta.get_field('username').exact('user2')
    ], OR)

    sql, params = node.as_sql(None, None)

    assert sql == "(username = %s OR username = %s)"
    assert params == ['user1', 'user2']

def test_as_sql_with_xor_and_no_support():
    node = WhereNode([User._meta.get_field('username').exact('testuser')], XOR)
    
    with pytest.raises(EmptyResultSet):
        node.as_sql(None, None)

def test_as_sql_with_negation():
    node = WhereNode([User._meta.get_field('username').exact('testuser')], AND)
    node.negated = True
    
    sql, params = node.as_sql(None, None)

    assert sql == "NOT (username = %s)"
    assert params == ['testuser']