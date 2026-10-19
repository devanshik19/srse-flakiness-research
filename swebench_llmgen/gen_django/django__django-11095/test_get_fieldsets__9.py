import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User

class TestBaseModelAdmin:

    @pytest.fixture
    def admin_instance(self):
        class TestAdmin(ModelAdmin):
            fieldsets = None
            
            def get_fields(self, request, obj=None):
                return ['username', 'email']
        
        return TestAdmin()

    def test_get_fieldsets_defaults(self, admin_instance):
        assert admin_instance.get_fieldsets(None) == [(None, {'fields': ['username', 'email']})]

    def test_get_fieldsets_with_fieldsets(self, admin_instance):
        admin_instance.fieldsets = [('Basic Info', {'fields': ['username']})]
        assert admin_instance.get_fieldsets(None) == [('Basic Info', {'fields': ['username']})]

    def test_get_fieldsets_with_none_fieldsets(self, admin_instance):
        admin_instance.fieldsets = None
        assert admin_instance.get_fieldsets(None) == [(None, {'fields': ['username', 'email']})]

    def test_get_fieldsets_empty_fieldsets(self, admin_instance):
        admin_instance.fieldsets = []
        assert admin_instance.get_fieldsets(None) == [(None, {'fields': ['username', 'email']})]