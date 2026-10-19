import copy
import json
import re
from functools import partial, update_wrapper
from urllib.parse import quote as urlquote
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.admin import helpers, widgets
from django.contrib.admin.decorators import display
from django.contrib.admin.exceptions import DisallowedModelAdminToField
from django.contrib.admin.utils import (
    NestedObjects,
    construct_change_message,
    flatten_fieldsets,
    get_deleted_objects,
    lookup_spawns_duplicates,
    model_format_dict,
    model_ngettext,
    quote,
    unquote,
)
from django.contrib.auth import get_permission_codename
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ValidationError
from django.urls import reverse
from django.template.response import TemplateResponse
import pytest

class TestModelAdmin:
    
    @pytest.fixture
    def user(self, db):
        user = User.objects.create_user(username='testuser', password='password')
        return user
    
    @pytest.fixture
    def model_admin(self):
        from django.contrib.admin import ModelAdmin
        # Create a simple subclass of ModelAdmin for testing purpose
        class TestAdmin(ModelAdmin):
            list_display = ['username']
            change_list_template = "admin/change_list.html"
            def get_changelist_instance(self, request):
                # Simulating the changelist instance with basic functionality
                return self

            def has_view_or_change_permission(self, request):
                return True
            
            def response_action(self, request, queryset):
                return None
            
            def get_actions(self, request):
                return {}
            
            def message_user(self, request, message, level):
                messages.success(request, message)

            def has_change_permission(self, request):
                return True
            
            def get_changelist_formset(self, request):
                from django.forms.models import BaseModelFormSet
                class FormSet(BaseModelFormSet):
                    pass
                return FormSet
            
            def _get_list_editable_queryset(self, request, prefix):
                return User.objects.all()
        
        return TestAdmin(model=None, admin_site=None)

    def test_changelist_view_get(self, user, model_admin, client):
        client.login(username='testuser', password='password')
        response = client.get(reverse('admin:auth_user_changelist'))
        assert isinstance(response, TemplateResponse)
        assert response.status_code == 200

    def test_changelist_view_post_no_selection(self, user, model_admin, client):
        client.login(username='testuser', password='password')
        response = client.post(reverse('admin:auth_user_changelist'), {'index': ''})
        assert response.status_code == 302  # redirect because no item was selected
        assert 'Items must be selected' in str(response.content)

    def test_changelist_view_post_with_selection(self, user, model_admin, client):
        user_1 = User.objects.create_user(username='user1', password='password')
        user_2 = User.objects.create_user(username='user2', password='password')
        client.login(username='testuser', password='password')
        
        response = client.post(reverse('admin:auth_user_changelist'), {
            helpers.ACTION_CHECKBOX_NAME: [user_1.pk, user_2.pk],
            'index': '',
        })
        assert response.status_code == 302  # successful redirection after handling action

    def test_changelist_view_permission_denied(self, user, model_admin, client):
        model_admin.has_view_or_change_permission = lambda req: False
        client.login(username='testuser', password='password')

        with pytest.raises(PermissionDenied):
            model_admin.changelist_view(client.get(reverse('admin:auth_user_changelist')))