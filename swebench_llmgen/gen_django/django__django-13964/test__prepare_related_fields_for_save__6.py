import pytest
from django.contrib.auth.models import User
from django.db import models

class TestModel(User):
    test_field = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

def test_prepare_related_fields_for_save_with_unsaved_related_object():
    instance = TestModel()
    related_instance = TestModel(username='related_user')
    
    # Assign related instance without saving it
    instance.test_field = related_instance
    
    with pytest.raises(ValueError, match="prohibited to prevent data loss due to unsaved related object 'test_field'."):
        instance._prepare_related_fields_for_save('save')

def test_prepare_related_fields_for_save_with_saved_related_object():
    related_instance = TestModel.objects.create(username='related_user')
    instance = TestModel(test_field=related_instance)
    
    # This should not raise an error as the related instance is saved
    try:
        instance._prepare_related_fields_for_save('save')
    except ValueError:
        pytest.fail("ValueError raised unexpectedly.")

def test_prepare_related_fields_for_save_auto_assign_pk():
    related_instance = TestModel.objects.create(username='related_user')
    instance = TestModel()
    
    # Assign saved related instance
    instance.test_field = related_instance
    
    # This should set the instance's test_field pk
    instance._prepare_related_fields_for_save('save')
    assert instance.test_field.pk == related_instance.pk

def test_prepare_related_fields_for_save_with_pk_change():
    related_instance = TestModel.objects.create(username='related_user')
    different_related_instance = TestModel.objects.create(username='another_user')
    
    instance = TestModel(test_field=related_instance)
    
    # Initially, the related instance is set
    instance._prepare_related_fields_for_save('save')
    
    # Change the test_field to a different related instance
    instance.test_field = different_related_instance
    
    # Expect an error due to pk change in relation
    with pytest.raises(ValueError, match="prohibited to prevent data loss due to unsaved related object 'test_field'."):
        instance._prepare_related_fields_for_save('save')