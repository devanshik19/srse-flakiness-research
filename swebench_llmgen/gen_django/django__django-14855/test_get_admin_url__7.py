import pytest
from django.contrib.admin.helpers import AdminReadonlyField
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.urls import NoReverseMatch, reverse
from django.db import models

# Create a test remote field
class TestRemoteField:
    model = User

@pytest.mark.parametrize("pk, expected", [
    (1, True),  # Assuming User with pk=1 exists
    (9999, False)  # Assuming User with pk=9999 does not exist
])
def test_get_admin_url(pk, expected):
    remote_field = TestRemoteField()
    try:
        remote_obj = User.objects.get(pk=pk)
    except ObjectDoesNotExist:
        remote_obj = None

    admin_readonly_field = AdminReadonlyField(None, None, None, None)
    
    if remote_obj:
        result = admin_readonly_field.get_admin_url(remote_field, remote_obj)
        assert expected == (f'<a href="{reverse("admin:auth_user_change", args=[remote_obj.pk])}">{remote_obj}</a>' in result)
    else:
        result = admin_readonly_field.get_admin_url(remote_field, remote_obj)
        assert result == str(remote_obj)