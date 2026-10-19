import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.fields import AddField

@pytest.mark.parametrize("model_name, name, expected_fragment", [
    ("user", "email", "user_email"),
    ("post", "title", "post_title"),
    ("comment", "body", "comment_body"),
])
def test_migration_name_fragment(model_name, name, expected_fragment):
    # Arrange
    field = NOT_PROVIDED  # Placeholder since we are not testing field functionality
    add_field_operation = AddField(model_name=model_name, name=name, field=field, preserve_default=False)

    # Act
    result = add_field_operation.migration_name_fragment()

    # Assert
    assert result == expected_fragment