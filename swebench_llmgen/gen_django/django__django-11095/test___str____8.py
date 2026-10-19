import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User

class TestModelAdmin(ModelAdmin):
    model = User

def test_model_admin_str():
    admin_instance = TestModelAdmin(User, None)
    expected_str = f"{User._meta.app_label}.{TestModelAdmin.__name__}"
    assert str(admin_instance) == expected_str