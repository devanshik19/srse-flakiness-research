import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User

class TestBaseModelAdmin:
    class TestAdmin(ModelAdmin):
        fieldsets = None

    def test_get_fieldsets_no_fieldsets(self):
        admin = self.TestAdmin(model=User, admin_site=None)
        result = admin.get_fieldsets(request=None)
        assert result == [(None, {'fields': admin.get_fields(request=None, obj=None)})]

    def test_get_fieldsets_with_fieldsets(self):
        admin = self.TestAdmin(model=User, admin_site=None)
        admin.fieldsets = [('Main', {'fields': ['username', 'email']})]
        result = admin.get_fieldsets(request=None)
        assert result == admin.fieldsets

    def test_get_fieldsets_empty_fieldsets(self):
        admin = self.TestAdmin(model=User, admin_site=None)
        admin.fieldsets = []
        result = admin.get_fieldsets(request=None)
        assert result == [(None, {'fields': admin.get_fields(request=None, obj=None)})]