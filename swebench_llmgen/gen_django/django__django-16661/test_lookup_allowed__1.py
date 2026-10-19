import pytest
from django.contrib.admin import site
from django.contrib.auth.models import User
from django.db import models
from django.contrib.admin.filters import SimpleListFilter

class TestModel(models.Model):
    name = models.CharField(max_length=100)

class TestAdmin(BaseModelAdmin):
    model = TestModel
    list_filter = ['name']

site.register(TestModel, TestAdmin)

@pytest.mark.parametrize(
    "lookup, value, expected",
    [
        ("name", "John", True),  # Direct local field lookup
        ("name__exact", "John", True),  # Exact lookup
        ("pk", 1, True),  # Primary key lookup
        ("nonexistent_field", "value", True),  # Nonexistent field should return True
        ("relatedmodel__name", "value", False),  # Relational lookup not in list_filter
    ],
)
def test_lookup_allowed(lookup, value, expected):
    admin = TestAdmin(TestModel, site)
    
    assert admin.lookup_allowed(lookup, value) == expected

def test_lookup_allowed_with_relationship():
    class RelatedModel(models.Model):
        testmodel = models.ForeignKey(TestModel, on_delete=models.CASCADE)
        description = models.CharField(max_length=100)

    class RelatedModelAdmin(BaseModelAdmin):
        model = RelatedModel
        list_filter = ['testmodel']

    site.register(RelatedModel, RelatedModelAdmin)

    admin = RelatedModelAdmin(RelatedModel, site)
    
    assert admin.lookup_allowed("testmodel__name", "value") is True  # Valid relational lookup