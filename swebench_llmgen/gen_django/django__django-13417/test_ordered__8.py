import pytest
from django.contrib.auth.models import User
from django.db.models.query import EmptyQuerySet

@pytest.fixture
def user_queryset():
    return User.objects.all()

def test_ordered_with_default_ordering(user_queryset):
    user_queryset.model._meta.ordering = ['username']
    assert user_queryset.ordered() is True

def test_ordered_with_order_by(user_queryset):
    user_queryset = user_queryset.order_by('username')
    assert user_queryset.ordered() is True

def test_ordered_with_empty_queryset():
    empty_queryset = EmptyQuerySet()
    assert empty_queryset.ordered() is True

def test_ordered_without_ordering(user_queryset):
    user_queryset.model._meta.ordering = []
    assert user_queryset.ordered() is False