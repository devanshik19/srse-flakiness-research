import pytest
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_get_pk_val():
    # Create a User instance
    user = User.objects.create(username='testuser', password='password')

    # Access the _get_pk_val method directly using the instance
    pk_value = user._get_pk_val()

    # Check if the primary key value returned is correct
    assert pk_value == user.pk

    # Test with meta parameter (should be the same because pk is unchanged)
    meta_pk_value = user._get_pk_val(meta=user._meta)
    assert meta_pk_value == pk_value