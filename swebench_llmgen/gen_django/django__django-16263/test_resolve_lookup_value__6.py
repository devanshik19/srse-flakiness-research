import pytest
from django.db.models import QuerySet
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_resolve_lookup_value_single_expression():
    user = User.objects.create(username='test_user')
    
    query = Query(User)
    resolved_value = query.resolve_lookup_value(user, can_reuse=False, allow_joins=False)
    
    assert resolved_value == user, "The resolved value should be the user instance."

def test_resolve_lookup_value_list_of_expressions():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    query = Query(User)
    resolved_values = query.resolve_lookup_value([user1, user2], can_reuse=False, allow_joins=False)
    
    assert list(resolved_values) == [user1, user2], "The resolved values should match the list of user instances."

def test_resolve_lookup_value_tuple_of_expressions():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    query = Query(User)
    resolved_values = query.resolve_lookup_value((user1, user2), can_reuse=False, allow_joins=False)
    
    assert list(resolved_values) == [user1, user2], "The resolved values should match the tuple of user instances."

def test_resolve_lookup_value_namedtuple():
    from collections import namedtuple

    UserTuple = namedtuple('UserTuple', ['user', 'other'])
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    query = Query(User)
    resolved_value = query.resolve_lookup_value(UserTuple(user1, user2), can_reuse=False, allow_joins=False)

    assert resolved_value == UserTuple(user1, user2), "The resolved value should match the namedtuple of user instances."