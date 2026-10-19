import pytest
from collections import Counter
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models.deletion import Collector
from django.db.models.deletion import DO_NOTHING

@pytest.fixture
def collector():
    return Collector(using='default')

@pytest.mark.parametrize(
    'keep_parents, collect_related, expected_fast_deletes, expected_collects',
    [
        (False, True, 0, 2),   # Regular flow without keeping parents, collecting related
        (True, True, 0, 2),    # Keeping parents
        (False, False, 0, 1),  # Without collecting related
    ]
)
def test_collect(collector, keep_parents, collect_related, expected_fast_deletes, expected_collects):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2', related_name=user1)
    
    assert collector.can_fast_delete([user1, user2]) is False  # Fast delete should not be possible

    collector.collect([user1, user2], keep_parents=keep_parents, collect_related=collect_related)

    assert len(collector.fast_deletes) == expected_fast_deletes
    assert len(collector.collects) == expected_collects

    if keep_parents:
        assert User.objects.filter(username='user1').exists()
    else:
        assert not User.objects.filter(username='user1').exists()
    
    assert User.objects.filter(username='user2').exists()

def test_collect_no_objects(collector):
    collector.collect([], keep_parents=False, collect_related=True)
    assert len(collector.fast_deletes) == 0
    assert len(collector.collects) == 0

def test_collect_with_fast_delete(collector):
    user1 = User.objects.create(username='user1')
    # Assuming can_fast_delete for user1 returns True
    collector.fast_deletes.append(user1)  # Manually forcing fast delete for the test.
    collector.collect([user1], keep_parents=False, collect_related=True)
    
    assert len(collector.fast_deletes) == 1  # Should count the fast delete

    assert User.objects.filter(username='user1').exists()  # Should remain