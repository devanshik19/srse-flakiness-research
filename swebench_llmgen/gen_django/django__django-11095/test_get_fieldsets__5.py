import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User

class TestBaseModelAdmin(ModelAdmin):
    fieldsets = None

class TestGetFieldsets:
    @pytest.mark.parametrize("fieldsets, expected", [
        (None, [(None, {'fields': []})]),
        ([('Basic Info', {'fields': ['username', 'email']})], [('Basic Info', {'fields': ['username', 'email']})]),
    ])
    def test_get_fieldsets(self, fieldsets, expected):
        # Arrange
        admin_instance = TestBaseModelAdmin()
        admin_instance.fieldsets = fieldsets
        
        # Act
        result = admin_instance.get_fieldsets(None, None)
        
        # Assert
        assert result == expected

    def test_get_fieldsets_with_empty_fieldsets(self):
        # Arrange
        admin_instance = TestBaseModelAdmin()
        admin_instance.fieldsets = []
        
        # Act
        result = admin_instance.get_fieldsets(None, None)
        
        # Assert
        assert result == [(None, {'fields': []})]