import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.base import Operation
from django.db.migrations.operations.models import ModelOperation

class MockOperation(Operation):
    def __init__(self, model_name):
        self.model_name = model_name
       
    def references_model(self, name, app_label):
        return self.model_name == name

def test_reduce_model_operation():
    model_operation = ModelOperation('UserModel')
    
    # Test case where operation references the model
    operation = MockOperation('UserModel')
    result = model_operation.reduce(operation, 'auth')
    assert result is False  # should return False because it references the model

    # Test case where operation does not reference the model
    operation = MockOperation('OtherModel')
    result = model_operation.reduce(operation, 'auth')
    assert result is True  # should return True because it does not reference the model