import pytest
from django.contrib.auth.models import User
from django.db.models.query import QuerySet

# Creating an EmptyQuerySet subclass for testing purposes
class EmptyQuerySet(QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

@pytest.mark.django_db
def test_ordered_with_empty_queryset():
    empty_queryset = EmptyQuerySet(User)
    assert empty_queryset.ordered() is True

@pytest.mark.django_db
def test_ordered_with_order_by():
    user_queryset = User.objects.order_by('username')
    assert user_queryset.ordered() is True

@pytest.mark.django_db
def test_ordered_with_default_ordering():
    class UserWithDefaultOrdering(User):
        class Meta:
            ordering = ['username']

    UserWithDefaultOrdering.objects.create(username='testuser1')
    UserWithDefaultOrdering.objects.create(username='testuser2')
    queryset = UserWithDefaultOrdering.objects.all()
    assert queryset.ordered() is True

@pytest.mark.django_db
def test_ordered_without_ordering():
    user_queryset = User.objects.none()
    assert user_queryset.ordered() is False

@pytest.mark.django_db
def test_ordered_with_extra_order_by():
    user_queryset = User.objects.extra(order_by=['username'])
    assert user_queryset.ordered() is True

@pytest.mark.django_db
def test_ordered_without_ordering_and_default_ordering():
    class ModelWithoutOrdering(User):
        class Meta:
            ordering = []

    queryset = ModelWithoutOrdering.objects.all()
    assert queryset.ordered() is False