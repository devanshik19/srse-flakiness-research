import pytest
from django.contrib.auth.models import User
from django.contrib.admin import ModelAdmin
from django.db import models

# Create a simple model for testing
class TestModel(models.Model):
    name = models.CharField(max_length=100)

class TestModelAdmin(ModelAdmin):
    model = TestModel
    ordering = ['name']

@pytest.fixture
def test_model_admin():
    return TestModelAdmin(TestModel, None)

@pytest.fixture
def create_test_data():
    User.objects.create(username='user1')
    User.objects.create(username='user2')
    User.objects.create(username='user3')

def test_get_queryset_no_ordering(test_model_admin, create_test_data):
    queryset = test_model_admin.get_queryset(None)
    assert queryset.count() == 3

def test_get_queryset_with_ordering(test_model_admin, create_test_data):
    test_model_admin.ordering = ['-name']
    queryset = test_model_admin.get_queryset(None)
    assert list(queryset.values_list('name', flat=True)) == ['user3', 'user2', 'user1']