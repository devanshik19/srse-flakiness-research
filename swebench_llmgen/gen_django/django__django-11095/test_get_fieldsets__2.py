import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User

class TestBaseModelAdmin(ModelAdmin):
    fieldsets = None

    def get_fields(self, request, obj):
        return ['username', 'email']

def test_get_fieldsets_with_fieldsets():
    admin = TestBaseModelAdmin()
    admin.fieldsets = [('User Info', {'fields': ['username', 'email']})]
    
    request = None  # Mock or use a real request if you need specifics
    obj = User(username='testuser', email='test@example.com')
    
    fieldsets = admin.get_fieldsets(request, obj)
    assert fieldsets == [('User Info', {'fields': ['username', 'email']})]

def test_get_fieldsets_without_fieldsets():
    admin = TestBaseModelAdmin()
    
    request = None
    obj = User(username='testuser', email='test@example.com')

    fieldsets = admin.get_fieldsets(request, obj)
    assert fieldsets == [(None, {'fields': ['username', 'email']})]