import pytest
from django.db import models
from django.db.migrations.operations.models import CreateModel

@pytest.fixture
def create_model_instance():
    return CreateModel(name='TestModel', fields=[], options={}, bases=[], managers=[])

def test_describe_returns_correct_string(create_model_instance):
    assert create_model_instance.describe() == "Create model TestModel"

def test_describe_returns_proxy_string(create_model_instance):
    create_model_instance.options['proxy'] = True
    assert create_model_instance.describe() == "Create proxy model TestModel"