import pytest
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.db.models.sql.query import Query

@pytest.fixture
def user_query():
    # Create a new Query instance with the User model
    user_queryset = User.objects.all()
    return user_queryset.query

def test_deferred_to_data_empty_deferred_loading(user_query):
    target = {}
    user_query.deferred_loading = ([], set())
    user_query.deferred_to_data(target)
    assert target == {}

def test_deferred_to_data_no_defer(user_query):
    target = {}
    user_query.deferred_loading = (['username', 'email'], set())
    user_query.deferred_to_data(target)
    assert len(target) == 1
    assert user_query.model in target
    assert 'username' in target[user_query.model]
    assert 'email' in target[user_query.model]

def test_deferred_to_data_with_defer(user_query):
    target = {}
    user_query.deferred_loading = (['username'], {'email'})
    user_query.deferred_to_data(target)
    assert len(target) == 1
    assert user_query.model in target
    assert 'username' in target[user_query.model]
    assert 'email' not in target[user_query.model]

def test_deferred_to_data_reverse_relation(user_query):
    target = {}
    user_query.deferred_loading = (['user__username'], set())
    user_query.deferred_to_data(target)
    assert user_query.model in target
    assert 'user' in target[user_query.model]

    # For the purposes of the test, simulate a reverse relation by adding more fields
    assert target[user_query.model]  # Check that the relations are accounted

def test_deferred_to_data_inheritance(user_query):
    target = {}
    user_query.deferred_loading = (['username', 'profile__bio'], {'email'})
    user_query.deferred_to_data(target)
    assert user_query.model in target
    assert 'username' in target[user_query.model]
    assert 'profile' in target[user_query.model]
    assert 'bio' not in target[user_query.model]