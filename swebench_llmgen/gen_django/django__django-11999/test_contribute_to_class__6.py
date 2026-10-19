import pytest
from django.contrib.auth.models import User
from django.db import models

class TestField(models.Field):
    def contribute_to_class(self, cls, name, private_only=False):
        super().contribute_to_class(cls, name, private_only)

def test_contribute_to_class_creates_field_in_model():
    field_name = 'test_field'
    test_field = TestField()

    # Contribute the field to the User model
    test_field.contribute_to_class(User, field_name)

    # Check that the field has been added to the User model
    assert hasattr(User, field_name)
    assert isinstance(getattr(User, field_name), models.Field)

def test_contribute_to_class_with_private_only():
    field_name = 'private_test_field'
    test_field = TestField()

    # Contribute the field with private_only set to True
    test_field.contribute_to_class(User, field_name, private_only=True)

    # Check that the field has been added to the User model
    assert hasattr(User, field_name)
    assert isinstance(getattr(User, field_name), models.Field)

def test_contribute_to_class_with_choices():
    field_name = 'choice_field'
    choices = [('1', 'Choice 1'), ('2', 'Choice 2')]
    test_field = TestField()
    test_field.choices = choices

    # Contribute the field to the User model
    test_field.contribute_to_class(User, field_name)

    # Check that the get_<field_name>_display method is added
    assert hasattr(User, 'get_%s_display' % field_name)
    display_method = getattr(User, 'get_%s_display' % field_name)

    # Check that calling the display method returns the choices correctly
    user = User.objects.create(username='testuser', password='password', **{field_name: '1'})
    assert user.get_choice_field_display() == 'Choice 1'