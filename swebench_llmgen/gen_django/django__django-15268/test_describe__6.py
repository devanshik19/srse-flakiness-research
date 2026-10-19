import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.models import CreateModel

def test_describe_with_proxy_option():
    operation = CreateModel(name='TestModel', fields=[], options={'proxy': True}, bases=[], managers=[])
    description = operation.describe()
    assert description == "Create proxy model TestModel"

def test_describe_without_proxy_option():
    operation = CreateModel(name='TestModel', fields=[], options={}, bases=[], managers=[])
    description = operation.describe()
    assert description == "Create model TestModel"