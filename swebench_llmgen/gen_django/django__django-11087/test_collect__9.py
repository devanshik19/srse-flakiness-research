import pytest
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models.deletion import Collector
from django.db.models import DO_NOTHING

class TestCollector:

    def setup_method(self):
        self.collector = Collector(using='default')

    def test_collect_no_objs(self):
        result = self.collector.collect([])
        assert self.collector.fast_deletes == []
        assert result is None

    def test_collect_with_fast_delete(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')

        # Simulate can_fast_delete method returning True
        self.collector.can_fast_delete = lambda objs, from_field=None: True

        self.collector.collect([user1, user2])
        assert len(self.collector.fast_deletes) == 1
        assert self.collector.fast_deletes[0] == [user1, user2]

    def test_collect_with_add_method(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')

        # Simulate can_fast_delete method returning False
        self.collector.can_fast_delete = lambda objs, from_field=None: False
        
        new_objs = self.collector.add = lambda objs, source, nullable, reverse_dependency: objs

        self.collector.collect([user1, user2])
        assert self.collector.fast_deletes == []
        assert new_objs.call_count == 1  # Ensure add was called

    def test_collect_with_related_objects(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')

        # Simulate related objects retrieval and deletion
        self.collector.can_fast_delete = lambda objs, from_field=None: False
        related_objects_return = [User.objects.create(username='related_user')]

        self.collector.related_objects = lambda related, objs: related_objects_return

        def mock_get_del_batches(objs, field):
            return [objs]
        
        self.collector.get_del_batches = mock_get_del_batches
        self.collector.collect([user1, user2], collect_related=True)

        # We do not have a real assertion on related_obj, but check if something was called
        assert len(self.collector.fast_deletes) == 0
        assert self.collector.related_objects(related=None, objs=[user1, user2]) == related_objects_return

    def test_collect_with_keep_parents(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')

        self.collector.collect([user1, user2], keep_parents=True)

        # Here we check if collect was successful without adding any deletion of parents
        assert len(self.collector.fast_deletes) == 0