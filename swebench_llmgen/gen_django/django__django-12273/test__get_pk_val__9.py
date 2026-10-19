import pytest
from django.contrib.auth.models import User
from django.db import models

class TestModelGetPkVal:

    def test_get_pk_val_with_default_meta(self):
        user = User(username='testuser')
        user.save()
        assert user._get_pk_val() == user.pk

    def test_get_pk_val_with_custom_meta(self):
        class CustomModel(User):
            class Meta:
                db_table = 'custom_user'

        custom_user = CustomModel(username='customuser')
        custom_user.save()
        assert custom_user._get_pk_val() == custom_user.pk

    def test_get_pk_val_not_found(self):
        user = User(username='nonexistent')
        with pytest.raises(AttributeError):
            user._get_pk_val(meta='invalid_meta')