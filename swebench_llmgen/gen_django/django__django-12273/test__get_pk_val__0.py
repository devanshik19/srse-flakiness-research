import pytest
from django.contrib.auth.models import User

def test_get_pk_val():
    # Create a user instance to test
    user = User(username='testuser', first_name='Test', last_name='User', email='test@example.com')
    user.save()

    # Test the primary key value retrieval
    assert user._get_pk_val() == user.pk

    # Test with meta parameter
    assert user._get_pk_val(meta=user._meta) == user.pk