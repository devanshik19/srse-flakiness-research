import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError

@pytest.fixture
def user_data():
    users = [
        User.objects.create(username='user1'),
        User.objects.create(username='user2'),
        User.objects.create(username='user3', email='user3@example.com'),
    ]
    return users

def test_in_bulk_with_id_list(user_data):
    user_ids = [user.pk for user in user_data]
    result = User.objects.in_bulk(user_ids)
    for user in user_data:
        assert result[user.pk] == user

def test_in_bulk_with_empty_id_list(user_data):
    result = User.objects.in_bulk([])
    assert result == {}

def test_in_bulk_without_id_list(user_data):
    result = User.objects.in_bulk()
    assert len(result) == len(user_data)
    for user in user_data:
        assert result[user.pk] == user

def test_in_bulk_with_non_unique_field(user_data):
    with pytest.raises(ValueError, match=r".*'username' must be a unique field but .* isn't."):
        User.objects.in_bulk(id_list=[user_data[0].pk, user_data[1].pk], field_name='username')

def test_in_bulk_with_non_existent_ids(user_data):
    # User with pk=999 does not exist
    user_ids = [user.pk for user in user_data] + [999]
    result = User.objects.in_bulk(user_ids)
    assert len(result) == len(user_data)
    for user in user_data:
        assert result[user.pk] == user