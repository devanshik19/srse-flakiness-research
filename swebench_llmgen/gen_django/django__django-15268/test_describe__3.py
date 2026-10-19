import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.models import CreateModel

def test_describe_without_proxy():
    create_model_operation = CreateModel("User", fields={}, options={}, bases=[], managers=[])
    assert create_model_operation.describe() == "Create model User"

def test_describe_with_proxy():
    create_model_operation = CreateModel("User", fields={}, options={"proxy": True}, bases=[], managers=[])
    assert create_model_operation.describe() == "Create proxy model User"