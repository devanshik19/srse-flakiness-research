import pytest
from django.contrib.auth.models import User
from django.db import transaction

@pytest.fixture
def user_db():
    users = [User.objects.create(username=f'user{i}') for i in range(5)]
    return users

def test_in_bulk_with_id_list(user_db):
    ids = [user.id for user in user_db]
    result = User.objects.in_bulk(ids)
    assert len(result) == len(user_db)
    for user in user_db:
        assert result[user.id] == user

def test_in_bulk_empty_id_list(user_db):
    result = User.objects.in_bulk(id_list=[])
    assert result == {}

def test_in_bulk_with_field_name(user_db):
    field_name = 'username'
    result = User.objects.in_bulk(id_list=[user.username for user in user_db], field_name=field_name)
    assert len(result) == len(user_db)
    for user in user_db:
        assert result[user.username] == user

def test_in_bulk_with_non_unique_field_name(user_db):
    with pytest.raises(ValueError):
        User.objects.in_bulk(id_list=[user.id for user in user_db], field_name='username')

def test_in_bulk_with_sliced_queryset(user_db):
    sliced_queryset = User.objects.all()[:3]
    with pytest.raises(AssertionError):
        sliced_queryset.in_bulk([user.id for user in user_db[:3]])

def test_in_bulk_with_large_id_list(user_db):
    large_ids = list(range(1, 1001))  # Assuming 1000 is larger than the database limit.
    for i in range(1, 1001):
        User.objects.create(username=f'user{i}')
    
    result = User.objects.in_bulk(id_list=large_ids)
    assert len(result) == 1000
    for user_id in large_ids:
        assert result[user_id] is not None