import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.template.response import TemplateResponse
from django.urls import reverse
from unittest.mock import MagicMock, patch

@pytest.fixture
def model_admin():
    admin_site = MagicMock()
    admin_site.name = "admin"
    return ModelAdmin(User, admin_site)

@pytest.fixture
def request_factory():
    return HttpRequest()

def test_changelist_view_permission_denied(model_admin, request_factory):
    request = request_factory
    request.method = "GET"
    request.user = User(is_staff=False)  # Not a staff user
    with pytest.raises(PermissionDenied):
        model_admin.changelist_view(request)

def test_changelist_view_invalid_lookup(model_admin, request_factory):
    request = request_factory
    request.method = "GET"
    request.user = User(is_staff=True)  # Staff user
    request.GET = MagicMock()
    request.GET.__contains__.side_effect = False  # Simulating invalid lookup parameters
    with patch('django.contrib.admin.views.main.ERROR_FLAG', "invalid"):
        response = model_admin.changelist_view(request)
        assert isinstance(response, HttpResponseRedirect)
        assert "invalid=1" in response.url

def test_changelist_view_no_action_selected(model_admin, request_factory):
    request = request_factory
    request.method = "POST"
    request.user = User(is_staff=True)
    request.POST = {
        'index': '',
        helpers.ACTION_CHECKBOX_NAME: []
    }
    with patch.object(model_admin, 'get_changelist_instance', return_value=MagicMock(result_list=[])) as mock_get_changelist:
        response = model_admin.changelist_view(request)
        assert response.status_code == 302  # Should redirect back
        model_admin.message_user.assert_called_with(
            request,
            "Items must be selected in order to perform actions on them. No items have been changed.",
            messages.WARNING
        )

def test_changelist_view_successful_action(model_admin, request_factory):
    request = request_factory
    request.method = "POST"
    request.user = User(is_staff=True)
    request.POST = {
        helpers.ACTION_CHECKBOX_NAME: [1],
        'index': ''
    }

    changelist_instance = MagicMock()
    changelist_instance.get_queryset.return_value = [User()]
    
    with patch.object(model_admin, 'get_changelist_instance', return_value=changelist_instance):
        with patch.object(model_admin, 'response_action', return_value=None) as mock_response_action:
            response = model_admin.changelist_view(request)
            mock_response_action.assert_called_once_with(request, queryset=changelist_instance.get_queryset.return_value)
            assert response is None  # Assuming redirect happens within response_action

def test_changelist_view_with_formset(model_admin, request_factory):
    request = request_factory
    request.method = "POST"
    request.user = User(is_staff=True)
    request.POST = {
        '_save': True
    }

    changelist_instance = MagicMock()
    changelist_instance.get_queryset.return_value = [User()]
    changelist_instance.list_editable = True
    
    FormSetMock = MagicMock()
    FormSetMock.return_value.is_valid.return_value = True
    FormSetMock.return_value.forms = [MagicMock(has_changed=lambda: True)]
    
    with patch.object(model_admin, 'get_changelist_instance', return_value=changelist_instance), \
         patch.object(model_admin, 'get_changelist_formset', return_value=FormSetMock):
        response = model_admin.changelist_view(request)

        FormSetMock.assert_called_once()
        assert response.status_code == 302  # Assuming it redirects after successful form processing