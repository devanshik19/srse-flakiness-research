import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.operations.models import CreateModel

@pytest.fixture
def create_model_instance():
    return CreateModel(name='User', fields=None, options={'proxy': False}, bases=None, managers=None)

def test_describe_with_proxy(create_model_instance):
    # Test when options['proxy'] is True
    create_model_instance.options['proxy'] = True
    assert create_model_instance.describe() == "Create proxy model User"

def test_describe_without_proxy(create_model_instance):
    # Test when options['proxy'] is False
    create_model_instance.options['proxy'] = False
    assert create_model_instance.describe() == "Create model User"