import pytest
from django.contrib.auth.models import User
from django.db.models import AutoField
from django.utils import six

class TestAutoFieldMeta:

    def setup_method(self):
        self.auto_field_meta = AutoField()  # Assuming this simulates AutoFieldMeta

    def test_instancecheck_valid_subclass(self):
        assert self.auto_field_meta.__instancecheck__(User) is True

    def test_instancecheck_invalid_class(self):
        assert self.auto_field_meta.__instancecheck__(str) is False

    def test_instancecheck_invalid_instance(self):
        class NotAUser:
            pass
        assert self.auto_field_meta.__instancecheck__(NotAUser()) is False

    def test_instancecheck_valid_instance(self):
        user = User(username='testuser')
        # Should return False for an instance of User at this point
        assert self.auto_field_meta.__instancecheck__(user) is True

    def test_instancecheck_multiple_subclasses(self):
        # Test with a subclass of User
        class CustomUser(User):
            pass
        assert self.auto_field_meta.__instancecheck__(CustomUser) is True
        assert self.auto_field_meta.__instancecheck__(CustomUser()) is True