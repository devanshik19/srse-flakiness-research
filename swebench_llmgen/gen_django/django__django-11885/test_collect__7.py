import pytest
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models.deletion import Collector
from django.db.models import DO_NOTHING
from unittest.mock import MagicMock

@pytest.fixture
def collector():
    return Collector(using='default')

def test_collect_fast_delete(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    collector.can_fast_delete = MagicMock(return_value=True)
    
    collector.collect([user1, user2])
    
    assert collector.fast_deletes == [[user1, user2]]

def test_collect_with_parents(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    collector.add = MagicMock(return_value=[user1, user2])
    collector.can_fast_delete = MagicMock(return_value=False)
    collector.collect_related = True
    
    collector.collect([user1, user2], keep_parents=False)

    # Check if add was called with expected parameters
    collector.add.assert_called_with([user1, user2], source=None, nullable=False, reverse_dependency=False)

def test_collect_keep_parents(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    collector.add = MagicMock(return_value=[user1, user2])
    collector.collect_related = True
    collector.collect([user1, user2], keep_parents=True)

    assert len(collector.fast_deletes) == 0

def test_collect_with_on_delete_action(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    collector.add = MagicMock(return_value=[user1, user2])
    collector.get_del_batches = MagicMock(return_value=[[user1, user2]])
    collector.related_objects = MagicMock(return_value=[user2])
    
    def custom_on_delete(collector, field, objs, using):
        collector.fast_deletes.append(objs)
        
    collector.related_objects = MagicMock(side_effect=custom_on_delete)

    collector.collect([user1, user2])

    assert len(collector.fast_deletes) > 0