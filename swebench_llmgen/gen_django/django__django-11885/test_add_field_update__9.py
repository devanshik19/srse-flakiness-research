import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

@pytest.fixture
def collector():
    return Collector(using='default')

def test_add_field_update_with_non_empty_objs(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    objs = [user1, user2]

    collector.add_field_update('email', 'user@example.com', objs)

    assert 'email' in collector.field_updates[User]
    assert ('email', 'user@example.com') in collector.field_updates[User]
    assert len(collector.field_updates[User][('email', 'user@example.com')]) == 2
    assert user1 in collector.field_updates[User][('email', 'user@example.com')]
    assert user2 in collector.field_updates[User][('email', 'user@example.com')]

def test_add_field_update_with_empty_objs(collector):
    objs = []
    
    collector.add_field_update('email', 'user@example.com', objs)
    
    assert 'email' not in collector.field_updates[User]