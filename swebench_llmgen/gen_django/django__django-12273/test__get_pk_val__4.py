import pytest
from django.contrib.auth.models import User

class TestModel:
    
    def test_get_pk_val(self):
        # Create a User instance
        user = User.objects.create_user(username='testuser', password='password')
        
        # Retrieve the _meta attribute to pass to the method
        meta = user._meta

        # Get the primary key value using the focal function
        pk_val = user._get_pk_val(meta)

        # Assert that the primary key value returned is equivalent to the user's id
        assert pk_val == user.id

    def test_get_pk_val_with_custom_meta(self):
        # Create another User instance
        user = User.objects.create_user(username='anotheruser', password='password')

        # Directly pass the meta information
        custom_meta = user._meta
        
        # Get the primary key value using the focal function with custom meta
        pk_val = user._get_pk_val(meta=custom_meta)

        # Assert that it matches the user's id
        assert pk_val == user.id