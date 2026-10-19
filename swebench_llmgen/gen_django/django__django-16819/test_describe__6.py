import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.operations.models import CreateModel

@pytest.mark.parametrize("options, expected", [
    ({}, "Create model User"),
    ({"proxy": True}, "Create proxy model User"),
])
def test_describe(options, expected):
    create_model_operation = CreateModel(name='User', fields=[], options=options, bases=[], managers=[])
    assert create_model_operation.describe() == expected