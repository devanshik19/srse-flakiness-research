import pytest
from django.contrib.auth.models import User

class AutoFieldMeta:
    def __init__(self):
        self._subclasses = (User,)

    def __instancecheck__(self, instance):
        return isinstance(instance, self._subclasses) or super().__instancecheck__(instance)

    def __subclasscheck__(self, subclass):
        return issubclass(subclass, self._subclasses) or super().__subclasscheck__(subclass)

def test_instancecheck_valid():
    auto_field_meta = AutoFieldMeta()
    assert auto_field_meta.__instancecheck__(User()) is True

def test_instancecheck_invalid():
    class NotUser:
        pass

    auto_field_meta = AutoFieldMeta()
    assert auto_field_meta.__instancecheck__(NotUser()) is False

def test_instancecheck_subclass():
    class CustomUser(User):
        pass

    auto_field_meta = AutoFieldMeta()
    assert auto_field_meta.__instancecheck__(CustomUser()) is True

def test_instancecheck_subclass_invalid():
    class AnotherClass:
        pass

    auto_field_meta = AutoFieldMeta()
    assert auto_field_meta.__instancecheck__(AnotherClass()) is False