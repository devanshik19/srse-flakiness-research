import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.models import ModelOperation

@pytest.fixture
def model_operation():
    return ModelOperation(name='User')

def test_references_model_true(model_operation):
    assert model_operation.references_model('User', 'auth') is True

def test_references_model_case_insensitive(model_operation):
    assert model_operation.references_model('user', 'auth') is True

def test_references_model_false(model_operation):
    assert model_operation.references_model('Group', 'auth') is False

def test_references_model_different_app(model_operation):
    assert model_operation.references_model('User', 'another_app') is True