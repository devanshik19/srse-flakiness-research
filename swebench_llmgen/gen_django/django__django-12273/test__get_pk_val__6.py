import pytest
from django.contrib.auth.models import User

class TestModel:

    def test_get_pk_val(self):
        # Create a User instance
        user = User(username='testuser')
        user.save()

        # Access the _get_pk_val method through the protected `_get_pk_val` interface
        pk_value = user._get_pk_val()  # Using the focal function directly

        # Check if the returned primary key value is correct
        assert pk_value == user.pk

    def test_get_pk_val_with_meta(self):
        user = User(username='testuser_meta')
        user.save()
        
        # Test _get_pk_val with a custom _meta argument
        pk_value_meta = user._get_pk_val(meta=user._meta) 
        
        # Check if the returned primary key value is correct with custom meta
        assert pk_value_meta == user.pk