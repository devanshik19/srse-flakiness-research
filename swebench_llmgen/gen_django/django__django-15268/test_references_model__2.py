import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.models import ModelOperation

@pytest.mark.django_db
def test_references_model():
    operation = ModelOperation(name='User')

    # Test case where name matches (case insensitive)
    assert operation.references_model('user', 'auth') is True

    # Test case where name does not match
    assert operation.references_model('admin', 'auth') is False

    # Test case where name has different casing
    assert operation.references_model('USER', 'auth') is True

    # Test case with different app_label (not relevant for the name match)
    assert operation.references_model('user', 'another_app') is True

    # Confirming that passing None or empty string also returns False
    assert operation.references_model(None, 'auth') is False
    assert operation.references_model('', 'auth') is False