import pytest
from django.contrib.admin.utils import NotRelationField
from django.core import checks
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.contrib.auth.models import User
from django.contrib.admin import ModelAdmin
from django.contrib.admin.checks import ModelAdminChecks

class TestModelAdminChecks:
    
    @pytest.fixture
    def model_admin(self):
        class MockAdmin(ModelAdmin):
            model = User
            
        return MockAdmin()

    def test_check_list_display_item_callable(self, model_admin):
        result = model_admin._check_list_display_item(model_admin, callable, "caller")
        assert result == []

    def test_check_list_display_item_has_attr(self, model_admin):
        result = model_admin._check_list_display_item(model_admin, 'username', "Username")
        assert result == []

    def test_check_list_display_item_m2m_field(self, model_admin):
        # Check against a ManyToManyField
        class ManyToManyUser(models.Model):
            groups = models.ManyToManyField('auth.Group')

        admin = ModelAdminChecks()
        admin.model = ManyToManyUser
        result = admin._check_list_display_item(admin, 'groups', "Groups")
        assert len(result) == 1
        assert result[0].id == 'admin.E109'

    def test_check_list_display_item_field_does_not_exist(self, model_admin):
        result = model_admin._check_list_display_item(model_admin, 'non_existent_field', "NonExistent")
        assert result == []

    def test_check_list_display_item_invalid_attr_or_method(self, model_admin):
        result = model_admin._check_list_display_item(model_admin, 'invalid_attr', "Invalid")
        assert len(result) == 1
        assert result[0].id == 'admin.E108'