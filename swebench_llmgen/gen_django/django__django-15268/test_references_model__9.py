import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.models import ModelOperation

@pytest.mark.parametrize("name, expected", [
    ("User", True),
    ("user", True),
    ("Admin", False),
    ("admin", False),
])
def test_references_model(name, expected):
    operation = ModelOperation("User")
    result = operation.references_model(name, "auth")
    assert result == expected