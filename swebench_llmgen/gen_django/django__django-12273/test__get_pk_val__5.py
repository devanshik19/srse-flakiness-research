import pytest
from django.contrib.auth.models import User

def test_get_pk_val():
    # Create a user instance
    user = User(username='testuser', email='test@example.com')
    user.save()

    # Retrieve pk value using _get_pk_val
    pk_val = user._get_pk_val()

    # Assert that the pk value is correct
    assert pk_val == user.pk

    # Test with meta provided
    from django.db.models.options import Options
    user_meta = Options(User)
    pk_val_with_meta = user._get_pk_val(meta=user_meta)

    # Assert that pk value with custom meta is also correct
    assert pk_val_with_meta == user.pk

    # Clean up by deleting the user instance
    user.delete()