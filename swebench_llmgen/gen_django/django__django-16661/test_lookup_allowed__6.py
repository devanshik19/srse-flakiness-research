import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User
from django.db import models

class TestModel(models.Model):
    name = models.CharField(max_length=100)

class TestModelAdmin(ModelAdmin):
    model = TestModel
    list_filter = ['name']

@pytest.mark.parametrize(
    "lookup, value, expected",
    [
        ("name", "test", True),
        ("related_model__name", "test", True),  # Assuming that related_model is a valid FK in TestModel
        ("invalid_field", "test", True),  # Invalid field is allowed
        ("name__exact", "test", True), 
        ("related_model__id", 1, False),  # Assuming related_model__id is not in list_filter
    ]
)
def test_lookup_allowed(lookup, value, expected):
    admin = TestModelAdmin(TestModel, None)
    assert admin.lookup_allowed(lookup, value) == expected