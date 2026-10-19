import pytest
from django.contrib.auth.models import User
from django.db.models.query import EmptyQuerySet

@pytest.mark.parametrize("extra_order_by, order_by, default_ordering, expected", [
    (None, None, None, False),  # No ordering
    ([], [], None, False),  # No ordering
    ([('name', 'ASC')], None, None, True),  # extra_order_by present
    (None, ['name'], None, True),  # order_by present
    (None, None, ['name'], True),  # default_ordering present
    (None, None, None, False),  # No ordering or defaults
])
def test_ordered(extra_order_by, order_by, default_ordering, expected):
    queryset = User.objects.all()
    
    # Mocking the queryset's attributes for testing
    queryset.query.extra_order_by = extra_order_by
    queryset.query.order_by = order_by
    queryset.query.default_ordering = default_ordering
    queryset.model._meta.ordering = default_ordering if default_ordering else []
    
    # Perform the test
    assert queryset.ordered() == expected

def test_ordered_empty_queryset():
    empty_queryset = EmptyQuerySet(model=User)
    assert empty_queryset.ordered() is True