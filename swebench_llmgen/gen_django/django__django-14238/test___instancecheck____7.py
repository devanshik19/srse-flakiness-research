import pytest
from django.contrib.auth.models import User

class AutoFieldMeta:
    _subclasses = (User,)

    def __instancecheck__(self, instance):
        return isinstance(instance, self._subclasses) or super().__instancecheck__(instance)

def test_instancecheck_with_user_instance():
    meta = AutoFieldMeta()
    user_instance = User()
    assert meta.__instancecheck__(user_instance) is True

def test_instancecheck_with_non_user_instance():
    meta = AutoFieldMeta()
    non_user_instance = object()  # Not a User instance
    assert meta.__instancecheck__(non_user_instance) is False

def test_instancecheck_with_subclass():
    class CustomUser(User):
        pass

    meta = AutoFieldMeta()
    custom_user_instance = CustomUser()
    assert meta.__instancecheck__(custom_user_instance) is True

def test_instancecheck_with_superclass():
    class NotAUser:
        pass

    meta = AutoFieldMeta()
    not_a_user_instance = NotAUser()
    assert meta.__instancecheck__(not_a_user_instance) is False