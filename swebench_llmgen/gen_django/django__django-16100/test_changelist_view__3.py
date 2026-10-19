import pytest
from django.urls import reverse
from django.contrib.admin import site
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template.response import SimpleTemplateResponse
from django.core.exceptions import PermissionDenied
from django.contrib.admin.options import ModelAdmin

@pytest.fixture
def user_with_permissions(db):
    user = User.objects.create_user(username='admin', password='password')
    user.is_staff = True
    user.is_superuser = True
    user.save()
    return user

@pytest.fixture
def model_admin(user_with_permissions):
    class TestModelAdmin(ModelAdmin):
        change_list_template = 'admin/change_list.html'
        
        def get_changelist_instance(self, request):
            return self.get_changelist(request)

    return TestModelAdmin(User, site)

@pytest.fixture
def request_factory():
    from django.test import RequestFactory
    return RequestFactory()

def test_changelist_view_success(request_factory, model_admin, user_with_permissions):
    request = request_factory.get(reverse('admin:auth_user_changelist'))
    request.user = user_with_permissions

    response = model_admin.changelist_view(request)

    assert isinstance(response, SimpleTemplateResponse)
    assert response.status_code == 200

def test_changelist_view_permission_denied(request_factory, model_admin):
    request = request_factory.get(reverse('admin:auth_user_changelist'))
    request.user = User.objects.create_user(username='user', password='password', is_staff=True)

    with pytest.raises(PermissionDenied):
        model_admin.changelist_view(request)

def test_changelist_view_invalid_parameters_redirect(request_factory, model_admin, user_with_permissions):
    request = request_factory.get(reverse('admin:auth_user_changelist') + '?invalid=1')
    request.user = user_with_permissions

    response = model_admin.changelist_view(request)

    assert isinstance(response, HttpResponseRedirect)
    assert 'invalid=1' in response.url

def test_changelist_view_action_with_selection(request_factory, model_admin, user_with_permissions):
    request = request_factory.post(reverse('admin:auth_user_changelist'), data={
        'action': 'delete_selected',
        'index': '',
        'action-checkbox-name': [1, 2]  # Simulate selecting some users
    })
    request.user = user_with_permissions

    response = model_admin.changelist_view(request)

    assert isinstance(response, HttpResponseRedirect)
    assert response.status_code == 302

def test_changelist_view_action_no_selection_message(request_factory, model_admin, user_with_permissions):
    request = request_factory.post(reverse('admin:auth_user_changelist'), data={
        'action': 'delete_selected',
        'index': '',
        'action-checkbox-name': []  # No user selected
    })
    request.user = user_with_permissions

    response = model_admin.changelist_view(request)

    assert isinstance(response, HttpResponseRedirect)
    assert messages.get_messages(request).unsorted[0].level == messages.WARNING
    assert "Items must be selected" in str(messages.get_messages(request).unsorted[0])

def test_changelist_view_post_bulk_edit_success(request_factory, model_admin, user_with_permissions):
    request = request_factory.post(reverse('admin:auth_user_changelist'), data={
        '_save': 'Save',
        'some_field_to_edit': 'new_value'  # Simulating bulk edit input
    })
    request.user = user_with_permissions

    response = model_admin.changelist_view(request)

    assert response.status_code == 200  # Check for successful processing of request