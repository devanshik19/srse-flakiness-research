import pytest
from django.contrib.admin import site
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import RequestFactory
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib import messages

@pytest.fixture
def user_with_permissions(db):
    user = User.objects.create_user(username='testuser', password='testpass')
    user.is_staff = True
    user.save()
    return user

@pytest.fixture
def request_factory():
    return RequestFactory()

@pytest.fixture
def admin_view(user_with_permissions, request_factory):
    from django.contrib.admin import ModelAdmin

    # Creating an instance of ModelAdmin for testing
    class TestAdmin(ModelAdmin):
        pass

    admin_instance = TestAdmin(User, site)
    return admin_instance

def test_changelist_view_permissions_denied(admin_view, request_factory):
    # Create a request without the required permissions
    request = request_factory.get('/')
    request.user = User.objects.create_user(username='testuser', password='testpass', is_staff=True)
    
    with pytest.raises(PermissionDenied):
        admin_view.changelist_view(request)

def test_changelist_view_redirects_on_invalid_params(admin_view, request_factory, user_with_permissions):
    request = request_factory.get(reverse('admin:auth_user_changelist'))
    request.user = user_with_permissions
    request.GET = {'invalid': '1'}
    
    response = admin_view.changelist_view(request)
    assert response.status_code == 302
    assert 'invalid_setup.html' in str(response.content)

def test_changelist_view_no_selected_items_action(admin_view, request_factory, user_with_permissions):
    request = request_factory.post(reverse('admin:auth_user_changelist'), {
        'index': '1',
    })
    request.user = user_with_permissions

    response = admin_view.changelist_view(request)
    
    assert response.status_code == 302
    assert messages.get_messages(request).some(msg for msg in messages.get_messages(request) if msg.level == messages.WARNING)
    assert _("Items must be selected in order to perform actions on them. No items have been changed.") in str(response.content)

def test_changelist_view_valid_action(admin_view, request_factory, user_with_permissions):
    # Assuming a bulk action 'delete' exists in the ModelAdmin actions.
    # This would require setting up actions; here we're just testing the flow if it were valid.
    request = request_factory.post(reverse('admin:auth_user_changelist'), {
        helpers.ACTION_CHECKBOX_NAME: ['1'],
        'action': 'delete',
        'index': '1'
    })
    request.user = user_with_permissions

    # Here we would need to simulate that the queryset returned some users
    # and also implement the action in the TestAdmin class.
    
    response = admin_view.changelist_view(request)
    
    assert response.status_code == 302  # Assuming the action redirects
    # Additional assertions can be added here based on the action's logic

def test_changelist_view_display(admin_view, request_factory, user_with_permissions):
    request = request_factory.get(reverse('admin:auth_user_changelist'))
    request.user = user_with_permissions
    
    response = admin_view.changelist_view(request)
    
    assert response.status_code == 200
    assert isinstance(response, TemplateResponse)
    assert 'admin/auth/user/change_list.html' in str(response.template_name)