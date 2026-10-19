import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User
from django.db import models

class TestModel(models.Model):
    name = models.CharField(max_length=100)

class TestModelAdmin(ModelAdmin):
    model = TestModel
    ordering = ['name']

def test_get_queryset_with_ordering():
    # Arrange
    admin = TestModelAdmin(TestModel, None)
    User.objects.create(username='user1')
    User.objects.create(username='user2')
    User.objects.create(username='user3')
    admin.model.objects.create(name='Charlie')
    admin.model.objects.create(name='Alice')
    admin.model.objects.create(name='Bob')

    request = type('Request', (object,), {})()  # Create a mock request
    # Set up ordering in the mock request
    admin.get_ordering = lambda req: ['name']

    # Act
    qs = admin.get_queryset(request)

    # Assert
    assert list(qs) == list(TestModel.objects.order_by('name'))

def test_get_queryset_without_ordering():
    # Arrange
    admin = TestModelAdmin(TestModel, None)
    User.objects.create(username='user1')
    admin.model.objects.create(name='Charlie')
    admin.model.objects.create(name='Alice')
    admin.model.objects.create(name='Bob')

    request = type('Request', (object,), {})()  # Create a mock request
    # Ensure no ordering in the mock request
    admin.get_ordering = lambda req: None

    # Act
    qs = admin.get_queryset(request)

    # Assert
    assert list(qs) == list(TestModel.objects.all())