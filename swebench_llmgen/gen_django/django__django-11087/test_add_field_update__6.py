import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

@pytest.mark.parametrize("field, value", [
    ('is_active', True),
    ('is_active', False),
])
def test_add_field_update(field, value):
    # Arrange
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    user3 = User.objects.create(username='user3')
    
    collector = Collector(using='default')

    # Act
    collector.add_field_update(field, value, [user1, user2, user3])
    
    # Assert
    assert field in collector.field_updates[User][(field, value)]
    assert len(collector.field_updates[User][(field, value)]) == 3

    # Check if the original users are stored correctly
    assert user1 in collector.field_updates[User][(field, value)]
    assert user2 in collector.field_updates[User][(field, value)]
    assert user3 in collector.field_updates[User][(field, value)]

def test_add_field_update_empty_objs():
    # Arrange
    collector = Collector(using='default')

    # Act
    collector.add_field_update('is_active', True, [])

    # Assert
    assert not collector.field_updates