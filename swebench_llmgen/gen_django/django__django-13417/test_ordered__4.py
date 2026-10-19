import pytest
from django.contrib.auth.models import User
from django.db.models.query import EmptyQuerySet

@pytest.mark.parametrize("order_by, default_ordering, expected", [
    ([], [], True),  # Empty QuerySet should be ordered
    (None, [], True),  # Empty QuerySet should be ordered
    (['name'], [], True),  # Ordered by name
    ([], ['name'], True),  # Default ordering
    (None, ['name'], True),  # Default ordering available
    (['name'], ['age'], True),  # Ordered by name with default ordering
    ([], [], False),  # Not ordered if no fields
])
def test_ordered(order_by, default_ordering, expected):
    # Create a QuerySet instance for the User model
    queryset = User.objects.none()  # Start with an empty queryset
    # Set the query attributes directly for testing
    queryset.query.order_by = order_by
    queryset.query.default_ordering = default_ordering
    queryset.query.extra_order_by = []

    # Directly check the ordered method
    assert queryset.ordered() == expected

def test_ordered_with_empty_queryset():
    empty_queryset = EmptyQuerySet()
    assert empty_queryset.ordered() is True