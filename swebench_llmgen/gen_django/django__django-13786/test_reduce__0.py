import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.models import ModelOperation

class TestModelOperation:
    def setup_method(self):
        self.model_operation = ModelOperation("User")
        self.other_model_operation = ModelOperation("Group")

    def test_reduce_references_model(self):
        operation = self.other_model_operation
        app_label = "auth"
        assert self.model_operation.reduce(operation, app_label) is False

    def test_reduce_does_not_reference_model(self):
        operation = ModelOperation("NonExistentModel")
        app_label = "auth"
        assert self.model_operation.reduce(operation, app_label) is True

    def test_reduce_super_reduce_called(self):
        operation = ModelOperation("User")  # Referencing the same model
        app_label = "auth"
        assert self.model_operation.reduce(operation, app_label) is True