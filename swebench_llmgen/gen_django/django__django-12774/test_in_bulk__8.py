import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError

@pytest.mark.django_db
def test_in_bulk_with_valid_id_list():
    # Arrange
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    user3 = User.objects.create(username='user3')

    qs = User.objects
    
    # Act
    result = qs.in_bulk(id_list=[user1.id, user2.id, user3.id])

    # Assert
    assert result[user1.id] == user1
    assert result[user2.id] == user2
    assert result[user3.id] == user3

@pytest.mark.django_db
def test_in_bulk_with_empty_id_list():
    # Arrange
    qs = User.objects
    
    # Act
    result = qs.in_bulk(id_list=[])

    # Assert
    assert result == {}

@pytest.mark.django_db
def test_in_bulk_with_non_unique_field():
    # Arrange
    User.objects.create(username='user1')
    
    # Act & Assert
    with pytest.raises(ValueError, match="in_bulk\\(\\)'s field_name must be a unique field"):
        User.objects.in_bulk(field_name='username')

@pytest.mark.django_db
def test_in_bulk_with_sliced_queryset():
    # Arrange
    User.objects.create(username='user1')
    User.objects.create(username='user2')
    
    qs = User.objects.all()[:1]  # Slicing

    # Act & Assert
    with pytest.raises(AssertionError, match="Cannot use 'limit' or 'offset' with in_bulk"):
        qs.in_bulk(id_list=[1, 2])

@pytest.mark.django_db
def test_in_bulk_batches_on_db_limit():
    # Arrange
    user_ids = [User.objects.create(username=f'user{i}').id for i in range(1, 1001)]
    qs = User.objects

    # Act
    result = qs.in_bulk(id_list=user_ids[:1000])  # Assuming the limit forces batching

    # Assert
    for user_id in user_ids[:1000]:
        assert result[user_id].username == f'user{user_id}'