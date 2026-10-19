import pytest
from django.contrib.admin.utils import ModelAdminChecks
from django.contrib.auth.models import User
from django.core import checks
from django.db import models


class TestModelAdminChecks:

    @pytest.fixture
    def model_admin_checks(self):
        return ModelAdminChecks()

    def test_callable_item(self, model_admin_checks):
        obj = User
        item = lambda x: x
        label = 'Test Label'
        result = model_admin_checks._check_list_display_item(obj, item, label)
        assert result == []

    def test_attribute_exists(self, model_admin_checks):
        obj = User
        item = 'username'
        label = 'Username'
        result = model_admin_checks._check_list_display_item(obj, item, label)
        assert result == []

    def test_attribute_does_not_exist(self, model_admin_checks):
        obj = User
        item = 'non_existent_field'
        label = 'Non Existent Field'
        result = model_admin_checks._check_list_display_item(obj, item, label)
        assert len(result) == 1
        assert result[0].id == 'admin.E108'
        assert "refers to 'non_existent_field'" in str(result[0])

    def test_field_does_not_exist(self, model_admin_checks):
        class FakeModel:
            _meta = type('Meta', (), {'app_label': 'app', 'object_name': 'FakeModel'})

        obj = FakeModel()
        item = 'non_existent_field'
        label = 'Non Existent Field'
        result = model_admin_checks._check_list_display_item(obj, item, label)
        assert result == []

    def test_field_is_many_to_many(self, model_admin_checks):
        class FakeModel:
            _meta = type('Meta', (), {'app_label': 'app', 'object_name': 'FakeModel'})
            many_to_many_field = models.ManyToManyField(User)

        obj = FakeModel()
        item = 'many_to_many_field'
        label = 'Many To Many Field'
        result = model_admin_checks._check_list_display_item(obj, item, label)
        assert len(result) == 1
        assert result[0].id == 'admin.E109'
        assert "must not be a ManyToManyField." in str(result[0])