import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User

class TestModelAdmin(ModelAdmin):
    model = User

def test_model_admin_str():
    admin_instance = TestModelAdmin(model=User, admin_site=None)
    expected_str = f"{User._meta.app_label}.{admin_instance.__class__.__name__}"
    assert str(admin_instance) == expected_str