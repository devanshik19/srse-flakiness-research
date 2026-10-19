import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

class TestCollector:
    def test_add_no_objs(self):
        collector = Collector(using='default')
        result = collector.add([])
        assert result == []

    def test_add_new_objs(self):
        collector = Collector(using='default')
        user1 = User(username='user1')
        user2 = User(username='user2')
        new_objs = [user1, user2]

        result = collector.add(new_objs)
        assert result == new_objs
        assert user1 in collector.data[User]
        assert user2 in collector.data[User]

    def test_add_existing_objs(self):
        collector = Collector(using='default')
        user1 = User(username='user1')
        user2 = User(username='user2')
        new_objs = [user1, user2]
        collector.add(new_objs)

        # Attempt to add user1 again
        result = collector.add([user1])
        assert result == []
        assert len(collector.data[User]) == 2

    def test_add_with_source_and_nullable(self):
        collector = Collector(using='default')
        user1 = User(username='user1')
        user2 = User(username='user2')
        new_objs = [user1, user2]
        
        result = collector.add(new_objs, source=user1, nullable=True)
        assert result == new_objs
        assert user1 in collector.data[User]
        assert user2 in collector.data[User]
        assert user1 in collector.dependencies

    def test_add_with_source_and_non_nullable(self):
        collector = Collector(using='default')
        user1 = User(username='user1')
        user2 = User(username='user2')
        new_objs = [user1, user2]
        
        result = collector.add(new_objs, source=user1, nullable=False)
        assert result == new_objs
        assert user1 in collector.data[User]
        assert user2 in collector.data[User]
        assert user1 in collector.dependencies
        assert user2 not in collector.dependencies[user1._meta.concrete_model]

    def test_add_reverse_dependency(self):
        collector = Collector(using='default')
        user1 = User(username='user1')
        user2 = User(username='user2')
        new_objs = [user1, user2]
        
        collector.add(new_objs, source=user1, nullable=False, reverse_dependency=True)
        assert user1 in collector.dependencies
        assert user2 in collector.dependencies[user2._meta.concrete_model]