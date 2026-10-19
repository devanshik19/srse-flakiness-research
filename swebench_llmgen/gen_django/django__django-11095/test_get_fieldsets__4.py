import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User

class TestBaseModelAdmin(ModelAdmin):
    fieldsets = None

    def get_fields(self, request, obj=None):
        return ['username', 'email']

    def get_fieldsets(self, request, obj=None):
        if self.fieldsets:
            return self.fieldsets
        return [(None, {'fields': self.get_fields(request, obj)})]

def test_get_fieldsets_no_fieldsets():
    admin = TestBaseModelAdmin(model=User)
    request = None  # Simulate a request object
    assert admin.get_fieldsets(request) == [
        (None, {'fields': ['username', 'email']})
    ]

def test_get_fieldsets_with_fieldsets():
    admin = TestBaseModelAdmin(model=User)
    admin.fieldsets = [('User Info', {'fields': ['username']}),]
    request = None  # Simulate a request object
    assert admin.get_fieldsets(request) == [
        ('User Info', {'fields': ['username']}),
    ]