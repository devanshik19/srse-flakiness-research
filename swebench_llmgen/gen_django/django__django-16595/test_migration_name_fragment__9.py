import pytest
from django.contrib.auth.models import User
from your_app.migrations.operations.fields import AddField  # Adjust import based on your actual app path

@pytest.mark.parametrize(
    "model_name, name, expected_fragment",
    [
        ("user", "email", "user_email"),
        ("profile", "age", "profile_age"),
        ("account", "balance", "account_balance")
    ]
)
def test_migration_name_fragment(model_name, name, expected_fragment):
    field = NOT_PROVIDED  # Replace with actual field if necessary
    add_field_operation = AddField(model_name=model_name, name=name, field=field, preserve_default=False)
    
    assert add_field_operation.migration_name_fragment() == expected_fragment