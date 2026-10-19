import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.models import CreateModel

def test_describe_with_proxy_option():
    create_model_operation = CreateModel(name='TestModel', fields=[], options={'proxy': True}, bases=[], managers=[])
    assert create_model_operation.describe() == "Create proxy model TestModel"

def test_describe_without_proxy_option():
    create_model_operation = CreateModel(name='TestModel', fields=[], options={'proxy': False}, bases=[], managers=[])
    assert create_model_operation.describe() == "Create model TestModel"

def test_describe_default_option():
    create_model_operation = CreateModel(name='DefaultModel', fields=[], options={}, bases=[], managers=[])
    assert create_model_operation.describe() == "Create model DefaultModel"