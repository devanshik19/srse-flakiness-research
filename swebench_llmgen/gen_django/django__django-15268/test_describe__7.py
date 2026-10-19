import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.operations.base import Operation
from django.db.migrations.state import ModelState
from django.db.migrations.utils import field_references, resolve_relation
from django.db.models.options import normalize_together
from django.utils.functional import cached_property
from django.db.migrations.operations.models import CreateModel

def test_describe_without_proxy():
    create_model_operation = CreateModel(name='User', fields=('username', 'email'), options={}, bases=(User,), managers=[])
    assert create_model_operation.describe() == "Create model User"

def test_describe_with_proxy():
    create_model_operation = CreateModel(name='User', fields=('username', 'email'), options={'proxy': True}, bases=(User,), managers=[])
    assert create_model_operation.describe() == "Create proxy model User"