import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models.deletion import Collector

@pytest.mark.parametrize("keep_parents, nullable, collect_related", [
    (False, False, True),
    (True, False, True),
    (False, True, True),
    (False, False, False),
    (True, False, False)
])
def test_collect(keep_parents, nullable, collect_related):
    # Create initial users
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    collector = Collector(using='default')

    # Collect users
    collector.collect([user1, user2], keep_parents=keep_parents, 
                      nullable=nullable, collect_related=collect_related)

    # Check if `fast_deletes` contains the correct objects
    if collector.can_fast_delete([user1, user2]):
        assert collector.fast_deletes == [[user1, user2]]
    else:
        assert collector.fast_deletes == []
    
    # Collect related objects depending on the collect_related value
    # No related objects for User model, so we ensure nothing else gets collected
    assert len(collector.fast_deletes) == 0

    # Additional checks for parent instances in case of not keeping parents
    if not keep_parents:
        assert user1 in collector.fast_deletes or user2 in collector.fast_deletes
    
    # Simulate cascading deletions by collecting again
    if collect_related:
        collector.collect([user1], keep_parents=keep_parents, 
                          nullable=False, collect_related=True)
        if not keep_parents:
            # Assume there could be related deletions (if existent)
            assert len(collector.fast_deletes) == 0