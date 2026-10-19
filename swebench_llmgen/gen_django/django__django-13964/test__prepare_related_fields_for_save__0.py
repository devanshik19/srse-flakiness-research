import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models

class TestModel(User):
    related_field = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

def test_prepare_related_fields_for_save_when_related_field_is_unsaved():
    user = User(username='testuser')
    user.save()  # Save user to ensure it has a primary key

    test_instance = TestModel(username='testmodel')
    test_instance.related_field = user  # Assign the unsaved related object

    with pytest.raises(ValueError, match="prohibited to prevent data loss due to unsaved related object 'related_field'"):
        test_instance._prepare_related_fields_for_save('save')

def test_prepare_related_fields_for_save_when_related_field_is_saved():
    user = User(username='testuser')
    user.save()  # Save user to ensure it has a primary key

    test_instance = TestModel(username='testmodel')
    test_instance.related_field = user  # Assign the saved related object
    test_instance._prepare_related_fields_for_save('save')
    assert test_instance.related_field.pk == user.pk  # Ensure related field is correct

def test_prepare_related_fields_for_save_when_related_field_is_null():
    test_instance = TestModel(username='testmodel')
    test_instance.related_field = None  # Assigning None to the related field
    test_instance._prepare_related_fields_for_save('save')  # No error should be raised