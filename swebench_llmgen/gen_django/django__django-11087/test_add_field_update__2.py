import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

def test_add_field_update():
    # Arrange
    collector = Collector(using='default')
    user1 = User.objects.create(username='user1', email='user1@example.com')
    user2 = User.objects.create(username='user2', email='user2@example.com')
    
    # Define field and value to update
    field = 'email'
    value = 'updated_email@example.com'
    objs = [user1, user2]

    # Act
    collector.add_field_update(field, value, objs)

    # Assert the field updates contain the correct model and field/value pairs
    assert field in collector.field_updates[User]
    assert (field, value) in collector.field_updates[User]
    assert len(collector.field_updates[User][(field, value)]) == 2
    assert user1 in collector.field_updates[User][(field, value)]
    assert user2 in collector.field_updates[User][(field, value)]

def test_add_field_update_no_objects():
    # Arrange
    collector = Collector(using='default')
    field = 'email'
    value = 'updated_email@example.com'
    objs = []

    # Act
    collector.add_field_update(field, value, objs)

    # Assert no updates scheduled
    assert len(collector.field_updates) == 0