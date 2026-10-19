import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.operations.models import CreateModel

def test_describe():
    # Test case for a normal CreateModel
    create_model_op = CreateModel(name='TestModel', fields=[], options={}, bases=[], managers=[])
    assert create_model_op.describe() == "Create model TestModel"

    # Test case for a CreateModel with proxy option
    create_model_op_proxy = CreateModel(name='TestModelProxy', fields=[], options={'proxy': True}, bases=[], managers=[])
    assert create_model_op_proxy.describe() == "Create proxy model TestModelProxy"