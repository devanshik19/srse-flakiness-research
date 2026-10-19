import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError, DatabaseError

class TestModel:

    @pytest.fixture
    def user_instance(self):
        user = User(username='testuser')
        user.save()
        return user

    @pytest.fixture
    def related_user(self):
        return User.objects.create(username='relateduser')

    def test_prepare_related_fields_for_save_with_unsaved_related_instance(self, user_instance):
        user_instance._meta.concrete_fields = [
            MockForeignKeyField(name='related_user', remote_field=MockRemoteField(multiple=False))
        ]
        # Attempting to save without the related user being saved should raise a ValueError
        with pytest.raises(ValueError) as excinfo:
            user_instance._prepare_related_fields_for_save('save')
        assert str(excinfo.value) == "save() prohibited to prevent data loss due to unsaved related object 'related_user'."

    def test_prepare_related_fields_for_save_with_saved_related_instance(self, user_instance, related_user):
        user_instance._meta.concrete_fields = [
            MockForeignKeyField(name='related_user', remote_field=MockRemoteField(multiple=False))
        ]
        user_instance.related_user = related_user  # Associated with saved user
        
        user_instance._prepare_related_fields_for_save('save')
        assert user_instance.related_user.pk == related_user.pk  # Check if related user pk is set

    def test_prepare_related_fields_for_save_with_changed_related_instance(self, user_instance, related_user):
        another_related_user = User.objects.create(username='anotherrelateduser')
        user_instance._meta.concrete_fields = [
            MockForeignKeyField(name='related_user', remote_field=MockRemoteField(multiple=False))
        ]
        user_instance.related_user = related_user
        user_instance._prepare_related_fields_for_save('save')
        
        # Now change the related instance
        user_instance.related_user = another_related_user
        user_instance._prepare_related_fields_for_save('save')

        assert user_instance.related_user.pk == another_related_user.pk  # Check if pk is updated
        

class MockRemoteField:
    def __init__(self, multiple=True):
        self.multiple = multiple

class MockForeignKeyField:
    def __init__(self, name, remote_field):
        self.name = name
        self.remote_field = remote_field
        self.attname = name + '_id'  # Simulate Django's ForeignKey behavior

    def is_relation(self):
        return True

    def is_cached(self, instance):
        return hasattr(instance, self.name) and getattr(instance, self.name) is not None

    def delete_cached_value(self, instance):
        delattr(instance, self.name, None)