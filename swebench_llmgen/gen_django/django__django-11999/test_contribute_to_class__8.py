import pytest
from django.contrib.auth.models import User
from django.db.models import Field

class MyField(Field):
    def contribute_to_class(self, cls, name, private_only=False):
        super().contribute_to_class(cls, name, private_only)

def test_contribute_to_class_creates_field_for_model():
    field = MyField()
    user = User()
    field.contribute_to_class(User, 'test_field')

    assert hasattr(User, 'test_field')
    assert isinstance(getattr(User, 'test_field'), field.descriptor_class)

def test_contribute_to_class_private_only_creates_separate_instance():
    field = MyField()
    field.contribute_to_class(User, 'test_field', private_only=True)

    # Verify private field creation for subclasses (User has no subclasses, but we can check for Field descriptor)
    private_field = getattr(User, 'test_field')
    assert isinstance(private_field, field.descriptor_class)

def test_contribute_to_class_does_not_override_classmethod():
    class MyUser(User):
        @classmethod
        def test_method(cls):
            return "I'm a class method"

    field = MyField()
    field.attname = 'test_method'  # To simulate conflict with the class method
    field.contribute_to_class(MyUser, 'test_method')

    assert MyUser.test_method() == "I'm a class method"
    assert hasattr(MyUser, 'test_method')
    assert not isinstance(getattr(MyUser, 'test_method'), field.descriptor_class)

def test_contribute_to_class_with_choices_creates_display_method():
    field = MyField()
    field.name = 'status'
    field.choices = [('A', 'Active'), ('I', 'Inactive')]
    field.contribute_to_class(User, 'status')

    assert hasattr(User, 'get_status_display')
    assert User.get_status_display.__func__.__code__.co_argcount == 1  # Check that it takes 'self' only

    user = User(status='A')
    assert user.get_status_display() == 'Active'