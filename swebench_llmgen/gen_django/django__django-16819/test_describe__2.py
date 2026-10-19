import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.operations.models import CreateModel

class TestCreateModel:

    @pytest.fixture
    def create_model(self):
        return CreateModel(name="TestModel", fields=[], options={"proxy": False}, bases=[], managers=[])

    def test_describe_with_standard_model(self, create_model):
        model_instance = create_model
        description = model_instance.describe()
        assert description == "Create model TestModel"

    def test_describe_with_proxy_model(self, create_model):
        model_instance = create_model
        model_instance.options["proxy"] = True
        description = model_instance.describe()
        assert description == "Create proxy model TestModel"