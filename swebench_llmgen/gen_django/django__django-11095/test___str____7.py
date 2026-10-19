import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User

class TestModelAdmin(ModelAdmin):
    model = User

def test_str_method():
    admin_instance = TestModelAdmin(User, None)
    expected_str = f'{User._meta.app_label}.{admin_instance.__class__.__name__}'
    assert str(admin_instance) == expected_str