import pytest
from django.contrib.auth.models import User
from django.db import models

class TestModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='test_model')

    def _prepare_related_fields_for_save(self, operation_name):
        # Original method code here as provided in the user input
        ...

def test_prepare_related_fields_for_save_with_unsaved_related_object():
    user = User(username='testuser')
    user.save()

    test_instance = TestModel(user=user)
    
    # Should not raise an error because the related user instance is saved
    try:
        test_instance._prepare_related_fields_for_save("save")
    except ValueError as e:
        pytest.fail(f"ValueError raised: {e}")

    # Now, create a new TestModel instance with an unsaved user
    unsaved_user = User(username='unsaved_user')

    test_instance_with_unsaved_user = TestModel(user=unsaved_user)

    # Ensure that saving this instance raises ValueError due to unsaved user
    with pytest.raises(ValueError) as excinfo:
        test_instance_with_unsaved_user._prepare_related_fields_for_save("save")
    
    assert str(excinfo.value) == "save() prohibited to prevent data loss due to unsaved related object 'user'."

def test_prepare_related_fields_for_save_with_saved_related_object():
    user = User.objects.create(username='saved_user')

    test_instance = TestModel(user=user)

    # Test that it sets the related field correctly if the relation is valid
    test_instance._prepare_related_fields_for_save("save")
    assert test_instance.user == user