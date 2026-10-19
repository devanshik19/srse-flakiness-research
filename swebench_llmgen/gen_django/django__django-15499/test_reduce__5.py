import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.models import ModelOperation

class TestModelOperation:

    @pytest.fixture
    def model_operation(self):
        return ModelOperation(name='my_model_operation')

    def test_reduce_with_no_operation(self, model_operation):
        operation = None
        app_label = 'auth'
        result = model_operation.reduce(operation, app_label)
        assert result is None

    def test_reduce_with_reducible_operation(self, model_operation):
        class FakeOperation:
            def __init__(self, app_label):
                self.app_label = app_label
        
            def reduce(self, operation, app_label):
                return True

        operation = FakeOperation(app_label='auth')
        app_label = 'auth'
        result = model_operation.reduce(operation, app_label)
        assert result is True

    def test_reduce_with_non_reducible_operation(self, model_operation):
        class NonReducibleOperation:
            def __init__(self, app_label):
                self.app_label = app_label
            
            def reduce(self, operation, app_label):
                return False

        operation = NonReducibleOperation(app_label='auth')
        app_label = 'auth'
        result = model_operation.reduce(operation, app_label)
        assert result is False

    def test_reduce_with_different_app_label(self, model_operation):
        class AnotherOperation:
            def __init__(self, app_label):
                self.app_label = app_label

            def reduce(self, operation, app_label):
                return None

        operation = AnotherOperation(app_label='different_app')
        app_label = 'auth'
        result = model_operation.reduce(operation, app_label)
        assert result is None