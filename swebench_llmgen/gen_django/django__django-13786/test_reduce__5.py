import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.models import ModelOperation

class TestModelOperation:
    
    @pytest.fixture
    def model_operation(self):
        return ModelOperation(name='auth.User')

    def test_reduce_when_references_model(self, model_operation):
        operation = MockOperation(references=True)
        result = model_operation.reduce(operation, 'auth')
        assert result is True

    def test_reduce_when_does_not_reference_model(self, model_operation):
        operation = MockOperation(references=False)
        result = model_operation.reduce(operation, 'auth')
        assert result is False

    def test_reduce_with_super_returning_none(self, model_operation):
        operation = MockOperation(references=False, super_return=None)
        result = model_operation.reduce(operation, 'auth')
        assert result is True

class MockOperation:
    def __init__(self, references, super_return=True):
        self._references = references
        self._super_return = super_return

    def references_model(self, name, app_label):
        return self._references

    def reduce(self, operation, app_label):
        return self._super_return