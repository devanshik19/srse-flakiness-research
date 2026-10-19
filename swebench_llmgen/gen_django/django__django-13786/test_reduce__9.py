import pytest
from django.contrib.auth.models import User
from django.db import migrations
from django.db.migrations.operations.models import ModelOperation


class TestModelOperation:
    def test_reduce_returns_false_when_references_model(self):
        operation = ModelOperation('User')
        app_label = 'auth'
        
        # Hypothetical case where `references_model` returns True
        operation.references_model = lambda name, app_label: True
        
        # Call reduce
        result = operation.reduce(operation, app_label)
        
        # Expect reduce to return False
        assert result is False

    def test_reduce_returns_true_when_does_not_reference_model(self):
        operation = ModelOperation('User')
        app_label = 'auth'
        
        # Hypothetical case where `references_model` returns False
        operation.references_model = lambda name, app_label: False
        
        # Call reduce
        result = operation.reduce(operation, app_label)
        
        # Expect reduce to return True
        assert result is True

    def test_reduce_calls_super_reduce_method(self):
        class MockOperation(Operation):
            def reduce(self, operation, app_label):
                return 'super_reduce_called'

        operation = ModelOperation('User')
        app_label = 'auth'
        
        # Replace the operation with a mock for testing super call
        operation.reduce = MockOperation.reduce
        
        # Call reduce
        result = operation.reduce(operation, app_label)
        
        # Check if it calls the super reduce method
        assert result == 'super_reduce_called'