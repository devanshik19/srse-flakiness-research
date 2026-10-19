import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User

class TestBaseModelAdmin:
    @pytest.fixture
    def admin_instance(self):
        class TestModelAdmin(ModelAdmin):
            fieldsets = None
            
        return TestModelAdmin()

    def test_get_fieldsets_no_fieldsets(self, admin_instance):
        request = None
        result = admin_instance.get_fieldsets(request)
        assert result == [(None, {'fields': []})]

    def test_get_fieldsets_with_fieldsets(self, admin_instance):
        request = None
        admin_instance.fieldsets = [('Basic Info', {'fields': ['username', 'email']})]
        result = admin_instance.get_fieldsets(request)
        assert result == [('Basic Info', {'fields': ['username', 'email']})]