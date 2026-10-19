import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

@pytest.fixture
def collector():
    return Collector(using='default')

def test_add_field_update_single_object(collector):
    user = User.objects.create(username='testuser1')
    collector.add_field_update('is_active', False, [user])
    assert (user in collector.field_updates[User]['is_active', False])

def test_add_field_update_multiple_objects(collector):
    user1 = User.objects.create(username='testuser1')
    user2 = User.objects.create(username='testuser2')
    collector.add_field_update('is_active', False, [user1, user2])
    assert (user1 in collector.field_updates[User]['is_active', False])
    assert (user2 in collector.field_updates[User]['is_active', False])

def test_add_field_update_empty_objs(collector):
    collector.add_field_update('is_active', False, [])
    assert len(collector.field_updates) == 0

def test_add_field_update_different_fields(collector):
    user1 = User.objects.create(username='testuser1')
    user2 = User.objects.create(username='testuser2')
    collector.add_field_update('is_active', False, [user1])
    collector.add_field_update('email', 'test@example.com', [user2])
    
    assert (user1 in collector.field_updates[User]['is_active', False])
    assert (user2 in collector.field_updates[User]['email', 'test@example.com'])
    assert ('is_active' in collector.field_updates[User])
    assert ('email' in collector.field_updates[User])