import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

def test_add_field_update():
    # Create test users
    user1 = User.objects.create(username='testuser1', email='test1@example.com')
    user2 = User.objects.create(username='testuser2', email='test2@example.com')
    
    # Create a collector instance
    collector = Collector(using='default')
    
    # Test adding field updates with a valid field and value
    collector.add_field_update('email', 'updated@example.com', [user1, user2])
    
    # Verify that field updates are scheduled properly
    assert 'django.contrib.auth.models.User' in collector.field_updates
    assert ('email', 'updated@example.com') in collector.field_updates['django.contrib.auth.models.User']
    assert {user1, user2} == collector.field_updates['django.contrib.auth.models.User'][('email', 'updated@example.com')]
    
    # Test calling with an empty iterable
    collector.add_field_update('username', 'updateduser', [])
    # Verify that no updates are added
    assert len(collector.field_updates['django.contrib.auth.models.User']) == 1  # Still only the previous update

    # Test that adding more field updates works correctly
    collector.add_field_update('username', 'anotheruser', [user1])
    assert ('username', 'anotheruser') in collector.field_updates['django.contrib.auth.models.User']
    assert {user1} == collector.field_updates['django.contrib.auth.models.User'][('username', 'anotheruser')]
    
    # Check that previous updates remain intact
    assert {user1, user2} == collector.field_updates['django.contrib.auth.models.User'][('email', 'updated@example.com')]