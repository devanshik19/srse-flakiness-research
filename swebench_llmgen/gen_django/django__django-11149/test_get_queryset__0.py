import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User
from django.db import models

class TestModel(models.Model):
    name = models.CharField(max_length=100)

class TestModelAdmin(ModelAdmin):
    model = TestModel

    def get_ordering(self, request):
        return ['name']

@pytest.fixture
def setUp_user_and_model():
    user = User.objects.create_user(username='testuser', password='testpass')
    TestModel.objects.create(name='Alice')
    TestModel.objects.create(name='Bob')
    return user

def test_get_queryset_with_ordering(setUp_user_and_model):
    user = setUp_user_and_model
    admin = TestModelAdmin(TestModel, None)
    
    # Act
    queryset = admin.get_queryset(None)

    # Assert
    assert queryset.count() == 2
    assert list(queryset) == list(TestModel.objects.order_by('name'))

def test_get_queryset_without_ordering(setUp_user_and_model):
    user = setUp_user_and_model
    admin = TestModelAdmin(TestModel, None)
    admin.get_ordering = lambda request: None  # Simulate no ordering
    
    # Act
    queryset = admin.get_queryset(None)

    # Assert
    assert queryset.count() == 2
    assert list(queryset) == list(TestModel.objects.all())