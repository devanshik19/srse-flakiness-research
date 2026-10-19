import pytest
from django.contrib.auth.models import User
from django.contrib import admin
from django.http import Http404
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.admin import ModelAdmin
from django.template.response import TemplateResponse

# Custom ModelAdmin for testing
class CustomModelAdmin(ModelAdmin):
    def has_view_or_change_permission(self, request):
        return True
    
    def has_change_permission(self, request):
        return True

    def get_changelist_formset(self, request):
        return admin.forms.BaseModelFormSet

    def get_changelist_instance(self, request):
        class DummyChangeList:
            def get_queryset(self, request):
                return User.objects.all()

            @property
            def result_list(self):
                return User.objects.all()

        return DummyChangeList()

@pytest.mark.parametrize("method, action_checkbox_name, expected_action_size", [
    ("POST", True, 1),
    ("POST", False, 0),
    ("GET", True, 0),
    ("GET", False, 0)
])
def test_changelist_view(client, method, action_checkbox_name, expected_action_size):
    admin_site = admin.site
    admin_site.register(User, CustomModelAdmin)

    user = User.objects.create_superuser(username='admin', password='admin', email='admin@example.com')
    
    client.login(username='admin', password='admin')
    changelist_url = reverse('admin:auth_user_changelist')
    
    if method == "POST":
        response = client.post(changelist_url, data={
            'action': 'delete_selected' if action_checkbox_name else '',
            helpers.ACTION_CHECKBOX_NAME: ['1'] if action_checkbox_name else []
        })
    else:
        response = client.get(changelist_url)

    assert response.status_code == 200
    assert isinstance(response, TemplateResponse)
    if method == "POST":
        assert len(response.context_data['cl'].result_list) == expected_action_size
    else:
        assert len(response.context_data['cl'].result_list) == User.objects.count()

def test_changelist_view_permission_denied(client):
    class NoPermissionModelAdmin(CustomModelAdmin):
        def has_view_or_change_permission(self, request):
            return False

    admin.site.unregister(User)
    admin.site.register(User, NoPermissionModelAdmin)

    user = User.objects.create_user(username='user', password='user')
    client.login(username='user', password='user')
    
    changelist_url = reverse('admin:auth_user_changelist')
    
    with pytest.raises(PermissionDenied):
        client.get(changelist_url)

def test_changelist_view_invalid_params(client):
    admin.site.unregister(User)
    admin.site.register(User, CustomModelAdmin)

    user = User.objects.create_superuser(username='admin', password='admin', email='admin@example.com')
    client.login(username='admin', password='admin')
    
    changelist_url = reverse('admin:auth_user_changelist')
    response = client.get(f"{changelist_url}?invalid_param=1")
    
    assert response.status_code == 302
    assert response.url.startswith(changelist_url)
    assert "invalid=1" in response.url