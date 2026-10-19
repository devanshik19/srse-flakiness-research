import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError

@pytest.mark.django_db
def test_in_bulk_with_valid_ids():
    # Create test users
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    # Call in_bulk with valid IDs
    result = User.objects.in_bulk(id_list=[user1.id, user2.id])
    
    assert len(result) == 2
    assert result[user1.id].username == 'user1'
    assert result[user2.id].username == 'user2'


@pytest.mark.django_db
def test_in_bulk_with_empty_id_list():
    result = User.objects.in_bulk(id_list=[])
    assert result == {}


@pytest.mark.django_db
def test_in_bulk_with_non_unique_field():
    User.objects.create(username='user1')
    User.objects.create(username='user2')
    
    with pytest.raises(ValueError) as excinfo:
        User.objects.in_bulk(id_list=['user1', 'user2'], field_name='username')
    
    assert "in_bulk()'s field_name must be a unique field but 'username' isn't." in str(excinfo.value)


@pytest.mark.django_db
def test_in_bulk_with_field_name_pk():
    user1 = User.objects.create(username='user1')
    
    result = User.objects.in_bulk(id_list=[user1.id], field_name='pk')
    
    assert len(result) == 1
    assert result[user1.id].username == 'user1'


@pytest.mark.django_db
def test_in_bulk_batches_for_large_id_list():
    users = [User.objects.create(username=f'user{i}') for i in range(1, 1050)]  # 1049 users
    ids = [user.id for user in users]

    result = User.objects.in_bulk(id_list=ids, field_name='pk')
    
    assert len(result) == 1049
    for user in users:
        assert result[user.id].username == user.username