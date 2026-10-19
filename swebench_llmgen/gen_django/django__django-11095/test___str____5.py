import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User
from django.db import models


class TestModelAdmin(ModelAdmin):
    model = User


@pytest.mark.parametrize("app_label, expected_output", [
    ("auth", "auth.TestModelAdmin"),
])
def test_model_admin_str(app_label, expected_output):
    admin_instance = TestModelAdmin(User, None)
    assert admin_instance.__str__() == expected_output