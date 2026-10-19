import pytest
from django.contrib.auth.models import User
from django.db.models.fields import AutoFieldMeta

@pytest.fixture
def auto_field_meta():
    return AutoFieldMeta()

def test_instancecheck_pass(auto_field_meta):
    # Create an instance of a subclass that should pass the check.
    class SubClass(AutoFieldMeta):
        pass

    instance = SubClass()
    assert auto_field_meta.__instancecheck__(instance) is True

def test_instancecheck_fail(auto_field_meta):
    # Create an instance of a class that should not pass the check.
    class AnotherClass:
        pass

    instance = AnotherClass()
    assert auto_field_meta.__instancecheck__(instance) is False

def test_instancecheck_user_model(auto_field_meta):
    # Check specifically with the User model as a known instance.
    user_instance = User(username='testuser')
    assert auto_field_meta.__instancecheck__(user_instance) is False