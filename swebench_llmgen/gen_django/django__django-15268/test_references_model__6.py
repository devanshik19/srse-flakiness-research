import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.models import ModelOperation

@pytest.mark.parametrize("name,expected", [
    ("User", True),
    ("user", True),
    ("ADMIN", False),
    ("Profile", False),
])
def test_references_model(name, expected):
    operation = ModelOperation("User")  # initiating with the name 'User'
    assert operation.references_model(name, None) == expected