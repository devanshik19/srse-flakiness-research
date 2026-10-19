import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.models import CreateModel

def test_describe_without_proxy():
    create_model_op = CreateModel(name='CustomUser', fields=[], options={})
    assert create_model_op.describe() == "Create model CustomUser"

def test_describe_with_proxy():
    create_model_op = CreateModel(name='CustomUser', fields=[], options={'proxy': True})
    assert create_model_op.describe() == "Create proxy model CustomUser"