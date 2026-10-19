import json
import pytest
from django.urls import reverse
from django.contrib.admin.sites import site
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.admin import ModelAdmin
from django.utils.translation import gettext as _

class TestModelAdmin(ModelAdmin):
    change_list_template = "admin/change_list.html"

@pytest.fixture
def user(db):
    user = User.objects.create_user(username='testuser', password='password')
    return user

@pytest.fixture
def admin_user(db):
    user = User.objects.create_user(username='admin', password='admin', is_staff=True, is_superuser=True)
    return user

def test_changelist_view_no_permission(client, admin_user):
    client.login(username='testuser', password='password')
    url = reverse('admin:auth_user_changelist')
    response = client.get(url)
    assert response.status_code == 403  # Forbidden

def test_changelist_view_with_permission(client, admin_user):
    client.login(username='admin', password='admin')
    url = reverse('admin:auth_user_changelist')
    response = client.get(url)
    assert response.status_code == 200  # OK

def test_changelist_redirect_on_invalid_params(client, admin_user):
    client.login(username='admin', password='admin')
    url = reverse('admin:auth_user_changelist') + "?invalid_param=123"
    response = client.get(url)
    assert isinstance(response, HttpResponseRedirect)
    assert "invalid=1" in response.url

def test_changelist_view_bulk_action_with_selection(client, admin_user):
    client.login(username='admin', password='admin')
    url = reverse('admin:auth_user_changelist')
    # To simulate a bulk action
    response = client.post(url, data={
        'action': 'delete_selected',
        'selected': [],
        'index': '1'
    })
    assert response.status_code == 302  # Redirect
    assert _("Items must be selected in order to perform actions on them.") in str(response.content)

def test_changelist_view_bulk_editing(client, admin_user):
    client.login(username='admin', password='admin')
    user = User.objects.create_user(username='testuser2', password='password')
    url = reverse('admin:auth_user_changelist')
    
    # Assuming we want to edit the bulk user
    response = client.post(url, data={
        'action': 'edit',
        'selected': [user.id],
        '_save': 'Save'
    })
    assert response.status_code == 200  # Should stay on the changelist

def test_changelist_view_process_post_valid(client, admin_user):
    client.login(username='admin', password='admin')
    user = User.objects.create_user(username='testuser3', password='password')
    url = reverse('admin:auth_user_changelist')

    # Simulate a POST request for bulk editing
    response = client.post(url, data={
        'index': '1',
        '_save': 'Save',
        'username': 'newusername'
    })
    assert response.status_code == 302  # Should redirect after saving
    user.refresh_from_db()
    assert user.username == 'newusername'