import pytest
from django.db.migrations.operations.models import CreateModel
from django.contrib.auth.models import User

def test_describe_with_proxy_option():
    create_model = CreateModel(name='MyModel', fields=[], options={'proxy': True}, bases=[], managers=[])
    description = create_model.describe()
    assert description == "Create proxy model MyModel"

def test_describe_without_proxy_option():
    create_model = CreateModel(name='MyModel', fields=[], options={'proxy': False}, bases=[], managers=[])
    description = create_model.describe()
    assert description == "Create model MyModel"