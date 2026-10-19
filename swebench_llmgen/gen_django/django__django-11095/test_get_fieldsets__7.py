import pytest
from django.contrib.admin import site
from django.contrib.auth.models import User
from django.contrib.admin.options import BaseModelAdmin


class TestBaseModelAdmin(BaseModelAdmin):
    fieldsets = None

    def get_fields(self, request, obj=None):
        return ['username', 'email']


def test_get_fieldsets_with_fieldsets():
    admin_instance = TestBaseModelAdmin()
    admin_instance.fieldsets = [('User Info', {'fields': ['username', 'email']})]

    request = None  # Mock or real request object as needed
    result = admin_instance.get_fieldsets(request)

    assert result == [('User Info', {'fields': ['username', 'email']})]


def test_get_fieldsets_without_fieldsets():
    admin_instance = TestBaseModelAdmin()
    admin_instance.fieldsets = None

    request = None  # Mock or real request object as needed
    result = admin_instance.get_fieldsets(request)

    assert result == [(None, {'fields': ['username', 'email']})]