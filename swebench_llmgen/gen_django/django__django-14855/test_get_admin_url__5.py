import pytest
from django.contrib.admin.helpers import AdminReadonlyField
from django.contrib.auth.models import User
from django.urls import reverse

@pytest.mark.parametrize("remote_obj, expected_url", [
    (User.objects.create(username='testuser1'), reverse('admin:auth_user_change', args=[1])),
    (User.objects.create(username='testuser2'), reverse('admin:auth_user_change', args=[2])),
])
def test_get_admin_url_valid(reverse, remote_obj, expected_url):
    admin_readonly_field = AdminReadonlyField(None, None, False, None)
    remote_field = User._meta.get_field('username')
    
    result = admin_readonly_field.get_admin_url(remote_field, remote_obj)
    assert result == f'<a href="{expected_url}">{remote_obj}</a>'

def test_get_admin_url_no_reverse_match():
    admin_readonly_field = AdminReadonlyField(None, None, False, None)
    remote_field = User._meta.get_field('username')
    remote_obj = User(pk=9999, username='nonexistentuser')  # Simulating a non-existent user with a PK
    
    result = admin_readonly_field.get_admin_url(remote_field, remote_obj)
    assert result == str(remote_obj)