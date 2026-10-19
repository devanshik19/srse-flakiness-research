import pytest
from django.db.migrations.operations.models import CreateModel
from django.contrib.auth.models import User

def test_describe_without_proxy():
    create_model_operation = CreateModel(name='User', fields=['username', 'email'], options={}, bases=(User,), managers=None)
    assert create_model_operation.describe() == "Create model User"

def test_describe_with_proxy():
    create_model_operation = CreateModel(name='User', fields=['username', 'email'], options={'proxy': True}, bases=(User,), managers=None)
    assert create_model_operation.describe() == "Create proxy model User"