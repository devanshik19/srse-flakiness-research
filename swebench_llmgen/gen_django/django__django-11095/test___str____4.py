import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User

class TestModelAdmin(ModelAdmin):
    model = User

def test_model_admin_str():
    admin = TestModelAdmin(User, None)
    expected_str = f"{admin.model._meta.app_label}.{admin.__class__.__name__}"
    assert str(admin) == expected_str