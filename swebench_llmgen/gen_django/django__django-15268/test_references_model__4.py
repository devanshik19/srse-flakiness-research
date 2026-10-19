import pytest
from django.contrib.auth.models import User
from your_module_path import ModelOperation  # Replace with the actual module path

@pytest.fixture
def model_operation():
    return ModelOperation(name='User')

def test_references_model_true(model_operation):
    assert model_operation.references_model('User', 'auth') is True

def test_references_model_false_case_sensitive(model_operation):
    assert model_operation.references_model('user', 'auth') is False

def test_references_model_different_model(model_operation):
    assert model_operation.references_model('Group', 'auth') is False