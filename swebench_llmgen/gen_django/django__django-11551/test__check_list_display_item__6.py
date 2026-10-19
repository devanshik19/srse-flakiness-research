import pytest
from django.contrib.admin.checks import ModelAdminChecks
from django.contrib.auth.models import User
from django.core import checks
from django.db import models

class TestModelAdminChecks:
    
    @pytest.fixture
    def admin_checks(self):
        return ModelAdminChecks()

    def test_check_callable_item(self, admin_checks):
        user = User()
        result = admin_checks._check_list_display_item(user, lambda x: x, 'my_item')
        assert result == []

    def test_check_attribute_exists(self, admin_checks):
        user = User()
        result = admin_checks._check_list_display_item(user, 'username', 'my_item')
        assert result == []

    def test_check_attribute_not_exists(self, admin_checks):
        user = User()
        result = admin_checks._check_list_display_item(user, 'non_existent_attr', 'my_item')
        assert len(result) == 1
        assert result[0].id == 'admin.E108'

    def test_check_field_exists(self, admin_checks):
        user = User()
        result = admin_checks._check_list_display_item(user, 'email', 'email_field')
        assert result == []

    def test_check_field_does_not_exist(self, admin_checks):
        user = User()
        result = admin_checks._check_list_display_item(user, 'non_existent_field', 'my_item')
        assert len(result) == 1
        assert result[0].id == 'admin.E108'

    def test_check_many_to_many_field(self, admin_checks):
        class TestModel:
            _meta = models.Options()
            _meta.fields = []
            model = User
            
            def __init__(self):
                pass
            
            def many_to_many_field(self):
                pass
        
        test_obj = TestModel()
        # Simulating ManyToManyField
        test_obj.model._meta.get_field = lambda x: models.ManyToManyField(User)

        result = admin_checks._check_list_display_item(test_obj, 'many_to_many_field', 'my_item')
        assert len(result) == 1
        assert result[0].id == 'admin.E109'