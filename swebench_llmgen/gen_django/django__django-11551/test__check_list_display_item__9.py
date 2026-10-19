import pytest
from django.contrib.admin.utils import ModelAdminChecks
from django.contrib.auth.models import User
from django.core import checks
from django.core.exceptions import FieldDoesNotExist
from django.db import models

class TestModelAdminChecks:

    @pytest.fixture
    def setup(self):
        self.admin_checks = ModelAdminChecks()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_check_list_display_item_callable(self, setup):
        result = self.admin_checks._check_list_display_item(self.user, callable(lambda: None), 'Test Label')
        assert result == []

    def test_check_list_display_item_has_attribute(self, setup):
        result = self.admin_checks._check_list_display_item(self.user, 'username', 'Test Label')
        assert result == []

    def test_check_list_display_item_has_model_attribute(self, setup):
        result = self.admin_checks._check_list_display_item(self.user, 'date_joined', 'Test Label')
        assert result == []

    def test_check_list_display_item_field_does_not_exist(self, setup):
        result = self.admin_checks._check_list_display_item(self.user, 'non_existent_field', 'Test Label')
        assert result == []

    def test_check_list_display_item_many_to_many_field(self, setup):
        field = models.ManyToManyField(User)
        self.user._meta.fields.append(field)
        result = self.admin_checks._check_list_display_item(self.user, field.name, 'Test Label')
        assert len(result) == 1
        assert result[0].id == 'admin.E109'

    def test_check_list_display_item_invalid(self, setup):
        result = self.admin_checks._check_list_display_item(self.user, 'invalid_field', 'Test Label')
        assert len(result) == 1
        assert result[0].id == 'admin.E108'
        assert "refers to 'invalid_field'" in str(result[0])