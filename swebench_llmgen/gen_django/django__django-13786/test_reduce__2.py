import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.models import ModelOperation

class TestModelOperation:
    def setup_method(self):
        self.operation = ModelOperation(name='User')
        self.app_label = 'auth'  # Using the 'auth' app where User model is defined

    def test_reduce_with_no_operation_references(self):
        mock_operation = User._meta.model._meta.app_label  # No references from mock_operation
        result = self.operation.reduce(mock_operation, self.app_label)
        assert result is True  # Should return True since there are no references

    def test_reduce_with_operation_references_model(self):
        # Create a hypothetical operation that references the 'User' model
        class MockOperation:
            def references_model(self, name, app_label):
                return name == 'User' and app_label == 'auth'
        
        mock_operation = MockOperation()
        result = self.operation.reduce(mock_operation, self.app_label)
        assert result is False  # Should return False since it references the model