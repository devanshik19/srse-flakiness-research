import pytest
from django.contrib.auth.models import User
from django.db import models

class TestModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def _prepare_related_fields_for_save(self, operation_name):
        # Ensure that a model instance without a PK hasn't been assigned to
        # a ForeignKey or OneToOneField on this model. If the field is
        # nullable, allowing the save would result in silent data loss.
        for field in self._meta.concrete_fields:
            if field.is_relation and field.is_cached(self):
                obj = getattr(self, field.name, None)
                if not obj:
                    continue
                if obj.pk is None:
                    if not field.remote_field.multiple:
                        field.remote_field.delete_cached_value(obj)
                    raise ValueError(
                        "%s() prohibited to prevent data loss due to unsaved "
                        "related object '%s'." % (operation_name, field.name)
                    )
                elif getattr(self, field.attname) is None:
                    setattr(self, field.attname, obj.pk)
                if getattr(obj, field.target_field.attname) != getattr(self, field.attname):
                    field.delete_cached_value(self)

def test_prepare_related_fields_for_save_with_unsaved_related_object():
    user = User(username='test_user')
    model_instance = TestModel(user=user)

    with pytest.raises(ValueError, match="prohibited to prevent data loss due to unsaved related object 'user'."):
        model_instance._prepare_related_fields_for_save('save')

def test_prepare_related_fields_for_save_with_saved_related_object():
    user = User.objects.create(username='test_user')
    model_instance = TestModel(user=user)
    
    # Save the model instance to have a valid primary key
    model_instance.save()

    # Ensure there is no error when calling the function after saving
    model_instance._prepare_related_fields_for_save('save')

def test_prepare_related_fields_for_save_with_modified_related_object():
    user1 = User.objects.create(username='test_user1')
    user2 = User.objects.create(username='test_user2')

    model_instance = TestModel(user=user1)
    model_instance.save()

    model_instance.user = user2
    model_instance._prepare_related_fields_for_save('save')

    # Ensure the user is updated
    assert model_instance.user == user2