import pytest
from django.contrib.auth.models import User
from django.db import models

class ModelOperation:
    def __init__(self, name):
        self.name = name
        self.name_lower = name.lower()

    def references_model(self, name, app_label):
        return name.lower() == self.name_lower

    def reduce(self, operation, app_label):
        pass  # Implementation not needed for this test

def test_references_model():
    operation = ModelOperation(name='User')

    # Test with matching model name (case-insensitive)
    assert operation.references_model('user', 'auth') is True

    # Test with non-matching model name
    assert operation.references_model('post', 'auth') is False

    # Test with matching model name (same case)
    assert operation.references_model('User', 'auth') is True

    # Test with different case variation
    assert operation.references_model('USER', 'auth') is True

    # Test with an irrelevant app label
    assert operation.references_model('user', 'another_app') is True
    assert operation.references_model('post', 'another_app') is False