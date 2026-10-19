import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.models import ModelOperation

class TestModelOperation:
    def setup_method(self):
        self.operation = ModelOperation('auth.User')

    def test_reduce_references_model(self):
        operation = ModelOperation('auth.User')
        assert self.operation.reduce(operation, 'auth') is True

    def test_reduce_does_not_reference_model(self):
        operation = ModelOperation('auth.AnotherModel')  # This can be any model not in app_label
        assert self.operation.reduce(operation, 'auth') is False