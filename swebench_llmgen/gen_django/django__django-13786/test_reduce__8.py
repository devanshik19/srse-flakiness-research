import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.models import ModelOperation

class TestModelOperation:
    def setup_method(self):
        self.operation = ModelOperation('auth.User')

    def test_reduce_references_model(self):
        other_operation = ModelOperation('auth.User')
        assert self.operation.reduce(other_operation, 'auth') is True

    def test_reduce_does_not_reference_model(self):
        other_operation = ModelOperation('auth.AnotherModel')
        assert self.operation.reduce(other_operation, 'auth') is False

    def test_reduce_with_super_class(self):
        # Assuming super().reduce returns None or False
        class MockOperation(ModelOperation):
            def reduce(self, operation, app_label):
                return None  # Simulating super().reduce

        mock_operation = MockOperation('auth.User')
        assert mock_operation.reduce(other_operation, 'auth') is True  # Should still refer to the model