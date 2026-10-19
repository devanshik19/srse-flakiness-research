import pytest
from django.contrib.admin.utils import ModelAdmin
from django.contrib.auth.models import User
from django.core import checks
from django.core.exceptions import FieldDoesNotExist
from django.db import models

class ModelAdminChecks:
    def _check_list_display_item(self, obj, item, label):
        if callable(item):
            return []
        elif hasattr(obj, item):
            return []
        elif hasattr(obj.model, item):
            try:
                field = obj.model._meta.get_field(item)
            except FieldDoesNotExist:
                return []
            else:
                if isinstance(field, models.ManyToManyField):
                    return [
                        checks.Error(
                            "The value of '%s' must not be a ManyToManyField." % label,
                            obj=obj.__class__,
                            id='admin.E109',
                        )
                    ]
                return []
        else:
            return [
                checks.Error(
                    "The value of '%s' refers to '%s', which is not a callable, "
                    "an attribute of '%s', or an attribute or method on '%s.%s'." % (
                        label, item, obj.__class__.__name__,
                        obj.model._meta.app_label, obj.model._meta.object_name,
                    ),
                    obj=obj.__class__,
                    id='admin.E108',
                )
            ]

@pytest.fixture
def model_admin():
    class DummyAdmin(ModelAdmin):
        model = User

    return DummyAdmin()

def test_check_list_display_item_callable(model_admin):
    checks_result = model_admin._check_list_display_item(model_admin, lambda x: x, 'Test Label')
    assert checks_result == []

def test_check_list_display_item_attribute(model_admin):
    checks_result = model_admin._check_list_display_item(model_admin, 'username', 'Test Label')
    assert checks_result == []

def test_check_list_display_item_field_does_not_exist(model_admin):
    checks_result = model_admin._check_list_display_item(model_admin, 'nonexistent_field', 'Test Label')
    assert checks_result == []

def test_check_list_display_item_many_to_many_field(model_admin):
    # Create a ManyToManyField in a dummy model for this test
    class DummyUser(User):
        groups = models.ManyToManyField('auth.Group', blank=True)

    admin_with_m2m = DummyAdmin()
    admin_with_m2m.model = DummyUser
    checks_result = admin_with_m2m._check_list_display_item(admin_with_m2m, 'groups', 'Test Label')
    assert len(checks_result) == 1
    assert checks_result[0].id == 'admin.E109'

def test_check_list_display_item_invalid_field(model_admin):
    checks_result = model_admin._check_list_display_item(model_admin, 'invalid_field', 'Test Label')
    assert len(checks_result) == 1
    assert checks_result[0].id == 'admin.E108'