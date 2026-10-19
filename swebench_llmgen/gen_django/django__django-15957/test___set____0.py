import pytest
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.db import models

class ForeignKeyDeferredAttribute:
    def __set__(self, instance, value):
        if instance.__dict__.get(self.field.attname) != value and self.field.is_cached(
            instance
        ):
            self.field.delete_cached_value(instance)
        instance.__dict__[self.field.attname] = value

class TestForeignKeyDeferredAttribute:
    @pytest.fixture
    def setup_user(self):
        self.field = models.ForeignKey(User, on_delete=models.CASCADE)
        self.fk_attr = ForeignKeyDeferredAttribute()
        self.fk_attr.field = self.field
        self.instance = User(username='testuser', email='test@example.com')
        self.instance.save()

    def test_set_new_value(self, setup_user):
        new_user = User(username='newuser', email='new@example.com')
        new_user.save()
        
        self.fk_attr.__set__(self.instance, new_user)
        assert self.instance.__dict__[self.field.attname] == new_user

    def test_set_existing_value(self, setup_user):
        original_user = self.instance
        self.fk_attr.__set__(self.instance, original_user)
        assert self.instance.__dict__[self.field.attname] == original_user

    def test_set_different_value_and_cache_behavior(self, setup_user):
        new_user = User(username='cacheduser', email='cached@example.com')
        new_user.save()
        
        self.fk_attr.__set__(self.instance, new_user)
        assert self.instance.__dict__[self.field.attname] == new_user
        
        # Verify that in case the original value was cached, it is deleted
        old_value = self.instance.__dict__[self.field.attname]
        self.fk_attr.__set__(self.instance, original_user)  # setting back to original
        assert self.instance.__dict__[self.field.attname] == original_user

        # Check if the old_value's cached state is now deleted
        with pytest.raises(FieldError):
            getattr(self.field, 'cached_value')  # Placeholder for checking cache behavior