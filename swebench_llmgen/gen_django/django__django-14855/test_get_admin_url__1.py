import pytest
from django.contrib.admin.helpers import AdminReadonlyField
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import format_html

@pytest.mark.parametrize("pk, expected_result", [
    (1, '<a href="/admin/auth/user/1/change/">testuser</a>'),  # assuming User with pk=1 exists and has a username 'testuser'
])
def test_get_admin_url_success(db, pk, expected_result):
    user = User.objects.create(username='testuser', pk=pk)
    remote_field = User._meta.get_field('username')
    readonly_field = AdminReadonlyField(None, None, None, None)
    
    assert readonly_field.get_admin_url(remote_field, user) == expected_result

@pytest.mark.parametrize("pk, expected_result", [
    (999, 'testuser'),  # Assuming no user with this pk exists
])
def test_get_admin_url_no_reverse_match(db, pk, expected_result):
    user = User(username='testuser', pk=pk)
    remote_field = User._meta.get_field('username')
    readonly_field = AdminReadonlyField(None, None, None, None)
    
    assert readonly_field.get_admin_url(remote_field, user) == expected_result