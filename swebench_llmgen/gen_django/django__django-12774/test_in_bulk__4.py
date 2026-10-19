import pytest
from django.contrib.auth.models import User
from django.db import transaction

@pytest.mark.django_db
def test_in_bulk_with_id_list():
    # Create test users
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    user3 = User.objects.create(username='user3')

    qs = User.objects.all()
    id_list = [user1.pk, user2.pk, user3.pk]

    result = qs.in_bulk(id_list)

    assert len(result) == 3
    assert result[user1.pk] == user1
    assert result[user2.pk] == user2
    assert result[user3.pk] == user3

def test_in_bulk_with_empty_id_list():
    qs = User.objects.all()
    result = qs.in_bulk(id_list=[])

    assert result == {}

def test_in_bulk_with_sliced_query_set():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    qs = User.objects.all()[:1]  # Sliced queryset to induce an AssertionError
    with pytest.raises(AssertionError):
        qs.in_bulk(id_list=[user1.pk, user2.pk])

def test_in_bulk_with_non_unique_field():
    user1 = User.objects.create(username='user1', email='test@example.com')
    user2 = User.objects.create(username='user2', email='test@example.com')

    qs = User.objects.all()
    
    with pytest.raises(ValueError, match="in_bulk()'s field_name must be a unique field"):
        qs.in_bulk(id_list=[user1.pk, user2.pk], field_name='email')

def test_in_bulk_without_id_list():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    qs = User.objects.all()
    result = qs.in_bulk()

    assert len(result) == 2
    assert result[user1.pk] == user1
    assert result[user2.pk] == user2