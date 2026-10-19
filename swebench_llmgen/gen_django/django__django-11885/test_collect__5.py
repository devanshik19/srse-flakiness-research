import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector
from django.db.models import DO_NOTHING

@pytest.fixture
def collector():
    return Collector(using='default')

def test_collect_basic(collector):
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    user1.userprofile_set.create()  # Assuming UserProfile has a foreign key to User

    # Collecting users for deletion
    collector.collect([user1, user2])
    
    # Fast delete should be empty since we're not enabling it here
    assert not collector.fast_deletes

def test_collect_with_parents(collector):
    user3 = User.objects.create(username='user3')
    user4 = User.objects.create(username='user4')
    user3.userprofile_set.create()  # Create related object

    # Collecting users without keeping parents
    collector.collect([user3], keep_parents=False)
    
    assert len(collector.fast_deletes) == 0  # Verify fast deletes
    assert len(collector.get_del_batches([user3], user3.userprofile_set.related_model._meta.fields)) == 1

def test_collect_with_keep_parents(collector):
    user5 = User.objects.create(username='user5')
    user5.userprofile_set.create()  # Create related object

    # Collecting users with keep_parents=True
    collector.collect([user5], keep_parents=True)

    # No fast deletes should happen
    assert not collector.fast_deletes

def test_collect_with_related(collector):
    user6 = User.objects.create(username='user6')
    user6.userprofile_set.create()  # Create related object
    
    collector.collect([user6], collect_related=True)
    
    # Make assertions based on related objects
    assert len(collector.fast_deletes) == 0
    # Check if related objects are targeted for deletion
    assert len(collector.get_del_batches([user6], user6.userprofile_set.related_model._meta.fields)) == 1

def test_collect_no_deletion_on_do_nothing(collector):
    from django.db.models import ForeignKey
    from django.db import models

    class TestModel(models.Model):
        user = ForeignKey(User, on_delete=DO_NOTHING)
    
    user7 = User.objects.create(username='user7')
    test_instance = TestModel.objects.create(user=user7)
    
    collector.collect([test_instance], collect_related=True)

    assert len(collector.fast_deletes) == 0  # DO_NOTHING prevents deletion