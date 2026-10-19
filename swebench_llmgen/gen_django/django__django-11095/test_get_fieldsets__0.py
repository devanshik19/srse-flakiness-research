import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User

class TestBaseModelAdmin(ModelAdmin):
    fieldsets = None

    def get_fields(self, request, obj=None):
        return ['username', 'email']

def test_get_fieldsets_with_fieldsets():
    admin_instance = TestBaseModelAdmin()
    admin_instance.fieldsets = [('User Info', {'fields': ['username', 'email']})]
    request = None  # Replace with an actual request if necessary
    fieldsets = admin_instance.get_fieldsets(request)
    assert fieldsets == [('User Info', {'fields': ['username', 'email']})]

def test_get_fieldsets_without_fieldsets():
    admin_instance = TestBaseModelAdmin()
    admin_instance.fieldsets = None
    request = None  # Replace with an actual request if necessary
    fieldsets = admin_instance.get_fieldsets(request)
    assert fieldsets == [(None, {'fields': ['username', 'email']})]