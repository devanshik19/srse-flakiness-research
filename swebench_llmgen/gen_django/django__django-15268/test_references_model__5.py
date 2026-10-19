import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.models import ModelOperation

@pytest.fixture
def model_operation():
    return ModelOperation(name='User')

def test_references_model_exact_match(model_operation):
    assert model_operation.references_model('User', 'auth') is True

def test_references_model_case_insensitive_match(model_operation):
    assert model_operation.references_model('user', 'auth') is True

def test_references_model_non_matching_name(model_operation):
    assert model_operation.references_model('Admin', 'auth') is False

def test_references_model_non_matching_case(model_operation):
    assert model_operation.references_model('ADMIN', 'auth') is False