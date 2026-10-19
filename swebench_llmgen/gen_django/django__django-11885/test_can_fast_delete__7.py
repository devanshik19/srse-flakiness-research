import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import Collector

class TestCollector:
    @pytest.fixture
    def collector(self):
        return Collector(using='default')

    def test_can_fast_delete_no_cascade(self, collector):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        assert collector.can_fast_delete([user1, user2]) is True

    def test_can_fast_delete_with_cascade(self, collector):
        class Parent(models.Model):
            pass

        class Child(models.Model):
            parent = models.ForeignKey(Parent, on_delete=models.CASCADE)

        parent = Parent.objects.create()
        child = Child.objects.create(parent=parent)
        
        assert collector.can_fast_delete([parent]) is False
        assert collector.can_fast_delete([child]) is False

    def test_can_fast_delete_with_no_signal_listeners(self, collector):
        user = User.objects.create(username='user3')
        assert collector.can_fast_delete(user) is True

    def test_can_fast_delete_with_do_nothing(self, collector):
        class Parent(models.Model):
            pass

        class Child(models.Model):
            parent = models.ForeignKey(Parent, on_delete=models.DO_NOTHING)

        parent = Parent.objects.create()
        child = Child.objects.create(parent=parent)
        
        assert collector.can_fast_delete([parent]) is True
        assert collector.can_fast_delete([child]) is True

    def test_can_fast_delete_private_fields(self, collector):
        class SomeModel(models.Model):
            private_field = models.JSONField()

        some_instance = SomeModel.objects.create(private_field={})
        assert collector.can_fast_delete([some_instance]) is False