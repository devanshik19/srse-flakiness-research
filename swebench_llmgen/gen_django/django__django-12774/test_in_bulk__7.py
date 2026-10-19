import pytest
from django.contrib.auth.models import User
from django.db import connections

@pytest.mark.django_db
def test_in_bulk():
    # Create test users
    user1 = User.objects.create(username='testuser1')
    user2 = User.objects.create(username='testuser2')
    user3 = User.objects.create(username='testuser3')

    # Test in_bulk with a valid list of IDs
    id_list = [user1.id, user2.id]
    result = User.objects.in_bulk(id_list)
    assert len(result) == 2
    assert result[user1.id] == user1
    assert result[user2.id] == user2

    # Test in_bulk with an empty list
    result = User.objects.in_bulk([])
    assert result == {}

    # Test in_bulk without an id_list to get all users
    result = User.objects.in_bulk(field_name='username')
    assert len(result) == 3
    assert result[user1.username] == user1
    assert result[user2.username] == user2
    assert result[user3.username] == user3

    # Test in_bulk with a non-unique field name
    with pytest.raises(ValueError, match="in_bulk\\(\\)'s field_name must be a unique field but 'username' isn't."):
        User.objects.in_bulk(field_name='username')

    # Test in_bulk with batch size check
    # Mocking a database limit, if necessary, you could adjust connection's features here
    batch_size = connections['default'].features.max_query_params // 2  # Assuming a small limit for testing
    id_list = list(range(1, batch_size + 3))  # Create a fake list of IDs
    created_users = [User.objects.create(username=f'user{i}') for i in id_list]

    result = User.objects.in_bulk(id_list)
    for user in created_users:
        assert result[user.id] == user