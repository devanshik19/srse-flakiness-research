import pytest
from django.contrib.admin import site
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import PermissionDenied

@pytest.fixture
def user_with_permissions(client):
    user = User.objects.create_user(username='testuser', password='password')
    user.is_superuser = True
    user.is_staff = True
    user.save()
    client.login(username='testuser', password='password')
    return user

def test_changelist_view_permission_denied(client):
    user = User.objects.create_user(username='testuser', password='password')
    user.is_superuser = False
    user.is_staff = True
    user.save()
    client.login(username='testuser', password='password')

    url = reverse('admin:auth_user_changelist')
    
    response = client.get(url)
    
    assert response.status_code == 403  # Check for permission denied

def test_changelist_view_with_invalid_parameters(user_with_permissions):
    url = reverse('admin:auth_user_changelist') + "?invalid_param=1"

    response = user_with_permissions.client.get(url)

    assert response.status_code == 302  # Check for redirect due to invalid parameters
    assert "invalid=1" in response.url  # Ensure the redirect has invalid query parameter

def test_changelist_view_get_request(user_with_permissions):
    url = reverse('admin:auth_user_changelist')
    
    response = user_with_permissions.client.get(url)

    assert response.status_code == 200  # Check successful retrieval of the changelist page
    assert 'auth/user/change_list.html' in [template.name for template in response.template_name]  # Check for the correct template

def test_changelist_view_post_action(user_with_permissions):
    User.objects.create_user(username='testuser1', password='password1')
    User.objects.create_user(username='testuser2', password='password2')

    url = reverse('admin:auth_user_changelist')
    
    response = user_with_permissions.client.post(url, {
        'action': 'delete_selected',
        'index': '0',
        'action_checkbox': ['1', '2'],  # Assuming user IDs are 1 and 2 for test users
    })

    assert response.status_code == 302  # Expect redirect after action
    assert User.objects.count() == 0  # Check users have been deleted

def test_changelist_view_post_without_selection(user_with_permissions):
    url = reverse('admin:auth_user_changelist')
    
    response = user_with_permissions.client.post(url, {
        'action': 'delete_selected',
        'index': '0',
    })

    assert response.status_code == 302  # Expect redirect due to no selection
    assert "must be selected" in str(response.content)  # Check warning message is present