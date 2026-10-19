import pytest
from django.contrib.auth.models import User
from django.db.models.fields.related_descriptors import ForeignKeyDeferredAttribute
from django.db import models

class TestForeignKeyDeferredAttribute:
    @pytest.fixture(autouse=True)
    def setup(self):
        class TestModel(models.Model):
            user = User.objects.first()  # Assume a User instance exists for testing
            my_field = ForeignKeyDeferredAttribute('user')

        self.instance = TestModel()
        self.instance.__dict__ = {}

        self.foreign_key_attr = ForeignKeyDeferredAttribute('user')

    def test_set_value_changes_dict(self):
        self.foreign_key_attr.__set__(self.instance, 1)
        assert self.instance.__dict__['user'] == 1

    def test_set_value_updates_cached_value(self):
        self.foreign_key_attr.__set__(self.instance, 1)
        assert self.instance.__dict__.get('user') == 1

        self.foreign_key_attr.__set__(self.instance, 2)
        assert self.instance.__dict__.get('user') == 2

    def test_set_value_deletes_cached_if_different(self):
        self.foreign_key_attr.__set__(self.instance, 1)
        assert 'user' in self.instance.__dict__

        original_value = self.instance.__dict__['user']
        self.foreign_key_attr.__set__(self.instance, 2)

        assert original_value != self.instance.__dict__['user']
        assert self.instance.__dict__['user'] == 2