import pytest
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_get_pk_val():
    # Create a user instance
    user = User.objects.create_user(username='testuser', password='password123')
    
    # Get the primary key value using the _get_pk_val method
    pk_val = user._get_pk_val()
    
    # Assert that the primary key value is as expected
    assert pk_val == user.pk

    # Test the method with meta argument
    meta = user._meta
    pk_val_with_meta = user._get_pk_val(meta=meta)
    
    # Assert that the primary key value with meta argument is also as expected
    assert pk_val_with_meta == user.pk