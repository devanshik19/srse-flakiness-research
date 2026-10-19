import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User

class TestBaseModelAdmin(ModelAdmin):
    fieldsets = None

def test_get_fieldsets_without_fieldsets():
    admin = TestBaseModelAdmin(model=User)
    request = None
    result = admin.get_fieldsets(request)
    expected_result = [(None, {'fields': admin.get_fields(request, None)})]
    assert result == expected_result

def test_get_fieldsets_with_fieldsets():
    admin = TestBaseModelAdmin(model=User)
    admin.fieldsets = [('Basic Info', {'fields': ['username', 'email']})]
    request = None
    result = admin.get_fieldsets(request)
    expected_result = admin.fieldsets
    assert result == expected_result