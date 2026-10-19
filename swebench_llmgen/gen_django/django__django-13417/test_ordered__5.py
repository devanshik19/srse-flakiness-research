import pytest
from django.contrib.auth.models import User
from django.db.models.query import EmptyQuerySet

def test_ordered_with_empty_queryset():
    qs = EmptyQuerySet()
    assert qs.ordered() is True

def test_ordered_with_default_ordering():
    class UserWithDefaultOrdering(User):
        class Meta:
            ordering = ['username']

    qs = UserWithDefaultOrdering.objects.all()
    assert qs.ordered() is True

def test_ordered_with_order_by():
    qs = User.objects.order_by('username')
    assert qs.ordered() is True

def test_ordered_without_ordering():
    qs = User.objects.all()
    assert qs.ordered() is False

def test_ordered_with_extra_order_by():
    qs = User.objects.extra(select={'custom_order': 'username'}).order_by('custom_order')
    assert qs.ordered() is True