import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.operations.base import Operation
from django.db.migrations.state import ModelState
from django.db.migrations.utils import field_references, resolve_relation
from django.db.models.options import normalize_together
from django.utils.functional import cached_property
from django.db.migrations.operations.models import CreateModel

@pytest.mark.django_db
class TestCreateModel:

    def test_describe_with_proxy_option(self):
        create_model = CreateModel(
            name='UserModel',
            fields=(('id', models.AutoField(primary_key=True)),),
            options={'proxy': True},
            bases=(User,),
            managers=()
        )
        assert create_model.describe() == "Create proxy model UserModel"

    def test_describe_without_proxy_option(self):
        create_model = CreateModel(
            name='UserModel',
            fields=(('id', models.AutoField(primary_key=True)),),
            options={'proxy': False},
            bases=(User,),
            managers=()
        )
        assert create_model.describe() == "Create model UserModel"