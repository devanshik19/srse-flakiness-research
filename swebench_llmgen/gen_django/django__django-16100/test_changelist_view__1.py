import pytest
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

@pytest.fixture
def user_with_permissions(db):
    user = User.objects.create_user(username='testuser', password='password')
    user.is_superuser = True
    user.is_staff = True
    user.save()
    return user

@pytest.fixture
def admin_site(db):
    class TestModelAdmin(admin.ModelAdmin):
        model = User
    return TestModelAdmin(User, admin.site)

def test_changelist_view_get(admin_site, client, user_with_permissions):
    client.login(username='testuser', password='password')
    response = client.get(reverse('admin:auth_user_changelist'))
    assert response.status_code == 200
    assert 'User' in str(response.content)

def test_changelist_view_post_no_permission(admin_site, client, user_with_permissions):
    client.login(username='testuser', password='password')
    response = client.post(reverse('admin:auth_user_changelist'), {})
    assert isinstance(response, HttpResponseRedirect)
    assert 'invalid=1' in response.url

def test_changelist_view_post_with_actions(admin_site, client, user_with_permissions):
    user1 = User.objects.create_user(username='testuser1', password='password')
    user2 = User.objects.create_user(username='testuser2', password='password')
    
    client.login(username='testuser', password='password')
    post_data = {
        'action': 'delete_selected',
        'select_across': '',
        'action_checkbox': [user1.pk, user2.pk],
    }
    
    response = client.post(reverse('admin:auth_user_changelist'), post_data)
    assert response.status_code == 302
    assert User.objects.filter(pk=user1.pk).count() == 0
    assert User.objects.filter(pk=user2.pk).count() == 0

def test_changelist_view_with_bulk_edit(admin_site, client, user_with_permissions):
    user1 = User.objects.create_user(username='testuser1', password='password', first_name='Test')
    user2 = User.objects.create_user(username='testuser2', password='password', first_name='User')
    
    client.login(username='testuser', password='password')
    
    post_data = {
        '_save': 'Save',
        'action_checkbox': [user1.pk, user2.pk],
        'first_name': ['NewName1', 'NewName2']
    }

    response = client.post(reverse('admin:auth_user_changelist'), post_data)
    assert response.status_code == 302
    user1.refresh_from_db()
    user2.refresh_from_db()
    assert user1.first_name == 'NewName1'
    assert user2.first_name == 'NewName2'

def test_changelist_view_permission_denied(admin_site, client):
    user = User.objects.create_user(username='testuser', password='password')
    client.login(username='testuser', password='password')
    with pytest.raises(PermissionDenied):
        client.get(reverse('admin:auth_user_changelist'))