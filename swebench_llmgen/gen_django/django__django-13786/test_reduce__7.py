import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.models import ModelOperation

class TestModelOperation:
    @pytest.fixture
    def model_operation(self):
        return ModelOperation(name="User")

    @pytest.fixture
    def other_operation(self):
        return ModelOperation(name="Profile")

    def test_reduce_no_references(self, model_operation, other_operation):
        assert model_operation.reduce(other_operation, "auth") is True

    def test_reduce_with_references(self, model_operation):
        assert model_operation.reduce(model_operation, "auth") is False

    def test_reduce_with_different_app_label(self, model_operation, other_operation):
        assert model_operation.reduce(other_operation, "accounts") is True