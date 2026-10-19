import pytest
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

@pytest.mark.django_db
def test_in_bulk_with_valid_id_list():
    # Create sample users
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    user3 = User.objects.create(username='user3')

    # Test in_bulk with a valid id_list
    qs = User.objects.all()
    result = qs.in_bulk(id_list=[user1.id, user2.id])

    assert result == {
        user1.id: user1,
        user2.id: user2,
    }

def test_in_bulk_with_empty_id_list():
    qs = User.objects.all()
    result = qs.in_bulk(id_list=[])

    assert result == {}

def test_in_bulk_without_id_list():
    # Create users
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    # Test in_bulk without id_list
    qs = User.objects.all()
    result = qs.in_bulk()

    assert result == {
        user1.id: user1,
        user2.id: user2,
    }

def test_in_bulk_with_invalid_field_name():
    qs = User.objects.all()
    with pytest.raises(ValueError):
        qs.in_bulk(field_name='non_unique_field')

def test_in_bulk_with_sliced_queryset():
    # Create users
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    qs = User.objects.all()[:1]  # Slicing the queryset
    with pytest.raises(AssertionError):
        qs.in_bulk(id_list=[user1.id, user2.id])