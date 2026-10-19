import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

def test_add_field_update_single_instance():
    collector = Collector(using='default')
    user = User.objects.create(username='testuser')
    collector.add_field_update('username', 'newusername', [user])
    
    assert user.username == 'newusername'
    assert len(collector.field_updates) == 1
    assert (User, 'username', 'newusername') in collector.field_updates

def test_add_field_update_multiple_instances():
    collector = Collector(using='default')
    user1 = User.objects.create(username='testuser1')
    user2 = User.objects.create(username='testuser2')
    collector.add_field_update('username', 'newgroupname', [user1, user2])
    
    assert user1.username == 'newgroupname'
    assert user2.username == 'newgroupname'
    assert len(collector.field_updates) == 1
    assert (User, 'username', 'newgroupname') in collector.field_updates

def test_add_field_update_empty_objects():
    collector = Collector(using='default')
    collector.add_field_update('username', 'newusername', [])
    
    assert len(collector.field_updates) == 0

def test_add_field_update_with_different_values():
    collector = Collector(using='default')
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    collector.add_field_update('username', 'newusername1', [user1])
    collector.add_field_update('username', 'newusername2', [user2])
    
    assert user1.username == 'newusername1'
    assert user2.username == 'newusername2'
    assert len(collector.field_updates) == 2
    assert (User, 'username', 'newusername1') in collector.field_updates
    assert (User, 'username', 'newusername2') in collector.field_updates