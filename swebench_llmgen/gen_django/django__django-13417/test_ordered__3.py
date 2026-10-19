import pytest
from django.contrib.auth.models import User
from django.db.models.query import QuerySet

def test_ordered_with_no_ordering():
    qs = User.objects.all()
    assert qs.ordered() is False

def test_ordered_with_order_by():
    qs = User.objects.order_by('username')
    assert qs.ordered() is True

def test_ordered_with_extra_order_by():
    qs = User.objects.extra(select={'order_key': 'username'}).order_by('order_key')
    assert qs.ordered() is True

def test_ordered_with_default_ordering():
    class CustomUserQuerySet(QuerySet):
        def ordered(self):
            return True

    qs = CustomUserQuerySet(User)
    qs.query.default_ordering = True
    qs.query.get_meta = lambda: type('Meta', (), {'ordering': True})()
    assert qs.ordered() is True

def test_ordered_with_empty_queryset():
    class EmptyQuerySet(QuerySet):
        pass

    empty_qs = EmptyQuerySet(User)
    assert empty_qs.ordered() is True