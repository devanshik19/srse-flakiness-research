import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.models import ModelOperation

@pytest.mark.parametrize("model_name, expected", [
    ("User", True),
    ("user", True),
    ("Group", False),
    ("group", False),
])
def test_references_model(model_name, expected):
    operation = ModelOperation(name="User")
    result = operation.references_model(model_name, app_label="auth")
    assert result == expected