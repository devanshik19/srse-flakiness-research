import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User

class TestModelAdmin(ModelAdmin):
    model = User

def test_str_method():
    model_admin = TestModelAdmin(model=User, admin_site=None)
    expected_output = f"{User._meta.app_label}.{model_admin.__class__.__name__}"
    assert str(model_admin) == expected_output