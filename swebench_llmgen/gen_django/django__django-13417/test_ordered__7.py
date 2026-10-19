import pytest
from django.contrib.auth.models import User
from django.db.models.query import EmptyQuerySet
from django.db.models.query import QuerySet

def test_ordered_with_empty_queryset():
    qs = EmptyQuerySet(User)
    assert qs.ordered() is True

def test_ordered_with_default_ordering():
    class CustomUserQuerySet(QuerySet):
        class Meta:
            ordering = ['username']

    qs = CustomUserQuerySet(User)
    assert qs.ordered() is True

def test_ordered_with_order_by():
    qs = User.objects.order_by('username')
    assert qs.ordered() is True

def test_ordered_with_extra_order_by():
    class CustomQuerySet(QuerySet):
        def extra_ordering(self):
            self.query.extra_order_by = ['email']
            return self

    qs = CustomQuerySet(User).extra_ordering()
    assert qs.ordered() is True

def test_ordered_without_ordering():
    qs = User.objects.none()
    assert qs.ordered() is False