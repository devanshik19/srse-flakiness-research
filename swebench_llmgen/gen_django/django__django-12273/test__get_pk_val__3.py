import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

def test_get_pk_val():
    # Create a User instance
    user = User.objects.create(username='testuser', password='testpassword')
    
    # Test case where meta is None
    assert user._get_pk_val() == user.pk

    # Test case where meta is passed
    meta = user._meta
    assert user._get_pk_val(meta) == user.pk

    # Modifying the primary key field for edge case verification
    user.pk = None  # Simulate an object without a primary key
    with pytest.raises(ObjectDoesNotExist):
        user._get_pk_val()

    # Cleanup - delete created user
    user.delete()