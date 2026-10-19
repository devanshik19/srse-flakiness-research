import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User

class TestBaseModelAdmin(ModelAdmin):
    fieldsets = None

    def get_fields(self, request, obj=None):
        return ['username', 'email']

def test_get_fieldsets_no_fieldsets():
    admin = TestBaseModelAdmin(model=User)
    request = None  # Assuming request is not used within the method for this test
    fieldsets = admin.get_fieldsets(request)
    assert fieldsets == [(None, {'fields': ['username', 'email']})]

def test_get_fieldsets_with_fieldsets():
    admin = TestBaseModelAdmin(model=User)
    admin.fieldsets = [('User Info', {'fields': ['username', 'email']})]
    request = None  # Assuming request is not used within the method for this test
    fieldsets = admin.get_fieldsets(request)
    assert fieldsets == [('User Info', {'fields': ['username', 'email']})]