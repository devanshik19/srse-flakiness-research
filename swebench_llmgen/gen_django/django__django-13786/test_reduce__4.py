import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.models import ModelOperation

class TestModelOperation:
    
    def setup_method(self):
        self.operation = ModelOperation('auth.user')

    def test_reduce_references_model(self):
        other_operation = ModelOperation('auth.group')
        assert self.operation.reduce(other_operation, 'auth') is False

    def test_reduce_does_not_reference_model(self):
        other_operation = ModelOperation('auth.user')
        assert self.operation.reduce(other_operation, 'auth') is True

    def test_reduce_with_different_app_label(self):
        other_operation = ModelOperation('auth.user')
        assert self.operation.reduce(other_operation, 'different_app') is False