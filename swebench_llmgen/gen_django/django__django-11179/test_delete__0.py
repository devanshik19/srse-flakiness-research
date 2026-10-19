import pytest
from collections import Counter
from operator import attrgetter
from django.db import IntegrityError, transaction
from django.contrib.auth.models import User
from django.db.models import signals, sql
from django.db.models.deletion import Collector

@pytest.fixture
def collector():
    return Collector(using='default')

def test_delete_single_instance(collector):
    user = User.objects.create(username='testuser', email='test@example.com')
    collector.data = {User: {user}}
    
    deleted_count, deleted_counter = collector.delete()
    
    assert deleted_count == 1
    assert deleted_counter == {User._meta.label: 1}
    assert User.objects.filter(pk=user.pk).count() == 0

def test_delete_multiple_instances(collector):
    users = [User.objects.create(username=f'testuser{i}', email=f'test{i}@example.com') for i in range(3)]
    collector.data = {User: set(users)}
    
    deleted_count, deleted_counter = collector.delete()
    
    assert deleted_count == 3
    assert deleted_counter == {User._meta.label: 3}
    assert User.objects.filter(pk__in=[user.pk for user in users]).count() == 0

def test_delete_fast_mode(collector):
    user = User.objects.create(username='testfastuser', email='testfast@example.com')
    collector.data = {User: {user}}
    
    def can_fast_delete(instance):
        return True
    
    collector.can_fast_delete = can_fast_delete
    
    deleted_count, deleted_counter = collector.delete()
    
    assert deleted_count == 1
    assert deleted_counter == {User._meta.label: 1}
    assert User.objects.filter(pk=user.pk).count() == 0

def test_delete_with_field_updates(collector):
    user = User.objects.create(username='testuser', email='test@example.com')
    collector.data = {User: {user}}
    collector.field_updates = {User: {('email', 'newemail@example.com'): {user}}}
    
    deleted_count, deleted_counter = collector.delete()
    
    assert deleted_count == 1
    assert deleted_counter == {User._meta.label: 1}
    assert User.objects.filter(pk=user.pk).count() == 0
    user.refresh_from_db()
    assert user.email == 'newemail@example.com'