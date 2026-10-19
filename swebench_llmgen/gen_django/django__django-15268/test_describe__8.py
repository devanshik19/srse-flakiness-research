import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.models import CreateModel

def test_describe_with_proxy_option():
    create_model = CreateModel(name='MyModel', fields=[], options={'proxy': True}, bases=[], managers=[])
    assert create_model.describe() == "Create proxy model MyModel"

def test_describe_without_proxy_option():
    create_model = CreateModel(name='MyModel', fields=[], options={'proxy': False}, bases=[], managers=[])
    assert create_model.describe() == "Create model MyModel"

def test_describe_without_proxy_option_default():
    create_model = CreateModel(name='MyModel', fields=[], options={}, bases=[], managers=[])
    assert create_model.describe() == "Create model MyModel"