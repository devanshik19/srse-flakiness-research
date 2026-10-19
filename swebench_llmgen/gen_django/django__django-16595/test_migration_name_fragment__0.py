import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.fields import AddField

@pytest.mark.parametrize(
    "model_name, field_name, expected_fragment",
    [
        ("user", "email", "user_email"),
        ("profile", "age", "profile_age"),
        ("post", "title", "post_title"),
    ]
)
def test_migration_name_fragment(model_name, field_name, expected_fragment):
    field = AddField(model_name=model_name, name=field_name, field=None, preserve_default=NOT_PROVIDED)
    assert field.migration_name_fragment() == expected_fragment