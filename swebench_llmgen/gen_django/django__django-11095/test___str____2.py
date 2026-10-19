import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User
from django.contrib.admin.sites import site

# Create a subclass of ModelAdmin for testing
class TestModelAdmin(ModelAdmin):
    model = User

def test_str_representation():
    admin_instance = TestModelAdmin(User, site)
    expected_str = f"{User._meta.app_label}.{admin_instance.__class__.__name__}"
    assert str(admin_instance) == expected_str