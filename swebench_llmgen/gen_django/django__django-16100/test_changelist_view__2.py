import pytest
from django.contrib.admin.sites import site
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.contrib.admin import ModelAdmin
from django.http.response import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

# Assuming a ModelAdmin subclass is created for the User model
class UserAdmin(ModelAdmin):
    model = User
    list_display = ['username', 'email']
    actions = ['delete_selected']

# Test cases for changelist_view
def test_changelist_view_without_permission():
    request = HttpRequest()
    request.method = 'GET'
    admin = UserAdmin(User, site)
    
    with pytest.raises(PermissionDenied):
        admin.changelist_view(request)

def test_changelist_view_with_invalid_lookup_parameters(client, admin_user):
    # Create user and log in
    client.force_login(admin_user)

    # Simulate an invalid request
    response = client.get('/admin/auth/user/?invalid=1')  # Example URL
    assert response.status_code == 302  # Redirect due to invalid parameters
    assert 'invalid=1' in response.url

def test_changelist_view_post_action_success(client, admin_user):
    # Create user and log in
    client.force_login(admin_user)
    user = User.objects.create_user(username='testuser', password='password')

    # Post an action with selected item
    response = client.post('/admin/auth/user/', {'action': 'delete_selected', 'index': '', helpers.ACTION_CHECKBOX_NAME: [user.pk]})
    assert response.status_code == 302  # Redirect after action
    assert User.objects.filter(username='testuser').count() == 0

def test_changelist_view_post_action_no_selection(client, admin_user):
    # Create user and log in
    client.force_login(admin_user)

    # Attempt to post an action with no selected items
    response = client.post('/admin/auth/user/', {'action': 'delete_selected', 'index': ''})
    assert response.status_code == 302  # Redirect after no action
    assert 'No items have been changed.' in str(response.content)

def test_changelist_view_post_edit_success(client, admin_user):
    # Create user and log in
    client.force_login(admin_user)
    user = User.objects.create_user(username='testuser', password='password')

    # Post bulk edit with change
    response = client.post('/admin/auth/user/', {
        'action': '', 'index': '', 
        '_save': '',
        'id': user.pk,
        'username': 'updateduser',
        'email': 'updated@example.com'
    })
    assert response.status_code == 302  # Redirect after editing
    user.refresh_from_db()
    assert user.username == 'updateduser'
    assert user.email == 'updated@example.com'

def test_changelist_view_get(client, admin_user):
    # Create user and log in
    client.force_login(admin_user)
    
    # Access the changelist view via GET
    response = client.get('/admin/auth/user/')
    assert response.status_code == 200
    assert 'User' in str(response.content)  # Ensures the change list is rendered