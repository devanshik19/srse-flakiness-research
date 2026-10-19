import pytest
from django.contrib.auth.models import User
from django.db import models

class ModelOperation:
    def __init__(self, name):
        self.name_lower = name.lower()

    def references_model(self, name, app_label):
        return name.lower() == self.name_lower

    def reduce(self, operation, app_label):
        # Placeholder implementation for other methods
        pass

def test_references_model():
    model_name = 'User'
    app_label = 'auth'
    operation = ModelOperation(model_name)

    assert operation.references_model('User', app_label) is True
    assert operation.references_model('user', app_label) is True
    assert operation.references_model('ADMIN', app_label) is False
    assert operation.references_model('another_model', app_label) is False