import pytest
from django.contrib.auth.models import User

class AutoFieldMeta:
    def _subclasses(self):
        return (User,)

    def __instancecheck__(self, instance):
        return isinstance(instance, self._subclasses()) or super().__instancecheck__(instance)

@pytest.fixture
def auto_field_meta():
    return AutoFieldMeta()

def test_instance_check_with_user(auto_field_meta):
    user_instance = User(username='testuser')
    assert auto_field_meta.__instancecheck__(user_instance) is True

def test_instance_check_with_non_user(auto_field_meta):
    non_user_instance = object()
    assert auto_field_meta.__instancecheck__(non_user_instance) is False

def test_instance_check_with_subclass(auto_field_meta):
    class CustomUser(User):
        pass

    custom_user_instance = CustomUser(username='customuser')
    assert auto_field_meta.__instancecheck__(custom_user_instance) is True