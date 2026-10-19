import pytest
from django.contrib.auth.models import User
from django.db.models.fields import AutoFieldMeta

def test_instancecheck_with_subclass():
    class CustomUser(User):
        pass

    meta = AutoFieldMeta()
    meta._subclasses = (User,)

    assert meta.__instancecheck__(User()) is True
    assert meta.__instancecheck__(CustomUser()) is True

def test_instancecheck_with_non_subclass():
    class NonUser:
        pass

    meta = AutoFieldMeta()
    meta._subclasses = (User,)

    assert meta.__instancecheck__(NonUser()) is False

def test_instancecheck_with_superclass():
    meta = AutoFieldMeta()
    meta._subclasses = (User,)

    assert meta.__instancecheck__(object()) is False