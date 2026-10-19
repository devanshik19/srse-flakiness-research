import pytest
from django.contrib.auth.models import User
from django.db.models.query import EmptyQuerySet

def test_ordered_with_empty_queryset():
    queryset = EmptyQuerySet(model=User)
    assert queryset.ordered() is True

def test_ordered_with_default_ordering():
    # Assuming User has default ordering defined in its Meta
    queryset = User.objects.all()
    assert queryset.ordered() is True  # Should return True with default ordering

def test_ordered_with_extra_order_by():
    queryset = User.objects.extra(select={'extra_order': 'id'}).order_by('username')
    assert queryset.ordered() is True  # Should return True with order_by()

def test_ordered_without_ordering():
    queryset = User.objects.none()
    assert queryset.ordered() is False  # Should return False without any ordering

def test_ordered_with_order_by():
    queryset = User.objects.order_by('username')
    assert queryset.ordered() is True  # Should return True with explicit order_by()