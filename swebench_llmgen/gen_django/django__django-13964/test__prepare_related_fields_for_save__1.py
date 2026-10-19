import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValueError
from django.db import models


class RelatedModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='related_model', null=True)


class TestModel(User):
    related = models.OneToOneField(RelatedModel, on_delete=models.SET_NULL, null=True, related_name='test_model')


@pytest.mark.parametrize("user_obj, expected_exception", [
    (None, ValueError),
    (User(pk=None), ValueError),  # Unsaved related object
    (User(pk=1), None),  # Saved related object
])
def test_prepare_related_fields_for_save(user_obj, expected_exception):
    # Create a test user and related model instance
    test_user = User.objects.create(username='testuser')
    related_instance = RelatedModel.objects.create(user=test_user)
    test_model_instance = TestModel(related=related_instance)

    if user_obj is not None:
        setattr(test_model_instance, 'related', user_obj)
    
    operation_name = "save"
    
    if expected_exception:
        with pytest.raises(expected_exception) as exc_info:
            test_model_instance._prepare_related_fields_for_save(operation_name)
        assert str(exc_info.value) == f"{operation_name}() prohibited to prevent data loss due to unsaved related object 'related'."
    else:
        test_model_instance._prepare_related_fields_for_save(operation_name)