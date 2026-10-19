import pytest
from django.contrib.auth.models import User
from django.db import models

class TestModel(User):

    def _prepare_related_fields_for_save(self, operation_name):
        super()._prepare_related_fields_for_save(operation_name)

def test_prepare_related_fields_for_save_no_related_object():
    user = TestModel()
    user._meta.concrete_fields = []
    user._prepare_related_fields_for_save("Test Save")
    # Test passes as there are no related fields

def test_prepare_related_fields_for_save_with_unsaved_related_object():
    related_user = User()
    user = TestModel()
    user._meta.concrete_fields = [models.OneToOneField(User, on_delete=models.CASCADE, related_name='related_user')]
    
    user.related_user = related_user  # Set the related field
    with pytest.raises(ValueError, match="prohibited to prevent data loss due to unsaved related object"):
        user._prepare_related_fields_for_save("Test Save")

def test_prepare_related_fields_for_save_with_saved_related_object():
    related_user = User.objects.create(username='testuser')
    user = TestModel.objects.create(username='testmodeluser')
    user.related_user = related_user  # Set the related field
    user._prepare_related_fields_for_save("Test Save")
    # Test passes as the related object is saved

def test_prepare_related_fields_for_save_with_changed_related_object():
    related_user1 = User.objects.create(username='testuser1')
    related_user2 = User.objects.create(username='testuser2')
    user = TestModel.objects.create(username='testmodeluser')
    user.related_user = related_user1  # Set the related field to the first user
    user._prepare_related_fields_for_save("Test Save")
    
    user.related_user = related_user2  # Change the related field
    user._meta.concrete_fields[0].delete_cached_value(user)  # Manually clear the cache
    user._prepare_related_fields_for_save("Test Save")
    # Test passes as it correctly handles changes in related object