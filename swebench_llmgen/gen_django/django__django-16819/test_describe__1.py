import pytest
from django.db.migrations.operations.models import CreateModel

@pytest.mark.parametrize("options, expected_description", [
    ({"proxy": False}, "Create model test_model"),
    ({"proxy": True}, "Create proxy model test_model"),
])
def test_describe(options, expected_description):
    create_model_operation = CreateModel(name="test_model", fields=[], options=options, bases=[], managers=[])
    assert create_model_operation.describe() == expected_description