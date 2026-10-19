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
        pass

def test_references_model():
    # Create an instance of ModelOperation with an example model name
    operation = ModelOperation('User')

    # Test case: should return True for matching case
    assert operation.references_model('User', 'auth') is True

    # Test case: should return True for matching lowercase
    assert operation.references_model('user', 'auth') is True

    # Test case: should return False for non-matching name
    assert operation.references_model('Profile', 'auth') is False

    # Test case: should return False for a completely different name
    assert operation.references_model('Product', 'shop') is False