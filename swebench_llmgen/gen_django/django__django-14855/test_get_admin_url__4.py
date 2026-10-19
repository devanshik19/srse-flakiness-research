import json
import pytest
from django import forms
from django.contrib.admin.utils import reverse, NoReverseMatch
from django.utils.html import format_html
from django.contrib.auth.models import User

class AdminReadonlyField:
    def __init__(self, form, field, is_first, model_admin):
        pass

    def get_admin_url(self, remote_field, remote_obj):
        url_name = 'admin:%s_%s_change' % (
            remote_field.model._meta.app_label,
            remote_field.model._meta.model_name,
        )
        try:
            url = reverse(url_name, args=[quote(remote_obj.pk)])
            return format_html('<a href="{}">{}</a>', url, remote_obj)
        except NoReverseMatch:
            return str(remote_obj)

# Fixtures
@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='password')

@pytest.fixture
def admin_readonly_field(user):
    class FakeModelAdmin:
        pass

    return AdminReadonlyField(form=None, field=None, is_first=True, model_admin=FakeModelAdmin())

@pytest.mark.parametrize("remote_field, expected_url", [
    (User._meta.get_field('username'), True),  # Will have a valid admin URL
])
def test_get_admin_url_valid(admin_readonly_field, remote_field, user):
    url = admin_readonly_field.get_admin_url(remote_field, user)
    assert '<a href=' in url
    assert f'">{user.username}</a>' in url

@pytest.mark.parametrize("invalid_remote_field, expected_output", [
    (None, 'testuser'),  # Simulate NoReverseMatch by passing None
])
def test_get_admin_url_invalid(admin_readonly_field, invalid_remote_field, user):
    output = admin_readonly_field.get_admin_url(invalid_remote_field, user)
    assert output == str(user)