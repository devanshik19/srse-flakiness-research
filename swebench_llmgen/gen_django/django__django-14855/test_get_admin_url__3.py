import pytest
from django.contrib.admin.helpers import AdminReadonlyField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.html import format_html


# Assuming a basic structure for a remote field representation
class RemoteField:
    def __init__(self, model):
        self.model = model


@pytest.fixture
def user_instance():
    user = User.objects.create(username='testuser', password='testpass')
    return user


@pytest.fixture
def readonly_field():
    return AdminReadonlyField(None, None, None, None)


def test_get_admin_url(valid_readonly_field, user_instance):
    remote_field = RemoteField(model=User)
    
    # Check for the valid case
    url = readonly_field.get_admin_url(remote_field, user_instance)
    expected_url = reverse('admin:auth_user_change', args=[user_instance.pk])
    
    assert url == format_html('<a href="{}">{}</a>', expected_url, user_instance)

    
def test_get_admin_url_no_reverse_match(readonly_field):
    class InvalidRemoteField:
        model = None

    remote_field = InvalidRemoteField()
    
    # This should fallback to just str(remote_obj)
    obj = "Invalid Object"
    url = readonly_field.get_admin_url(remote_field, obj)
    
    assert url == "Invalid Object"