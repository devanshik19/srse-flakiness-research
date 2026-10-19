import pytest
from django.contrib.auth.models import User
from django.db.migrations.operations.fields import AddField

class TestAddField:
    def test_migration_name_fragment(self):
        model_name = 'User'
        field_name = 'username'
        add_field_operation = AddField(model_name=model_name, name=field_name, field=None, preserve_default=NOT_PROVIDED)

        # Lowercase versions of model_name and field_name
        expected_fragment = f"{model_name.lower()}_{field_name.lower()}"
        assert add_field_operation.migration_name_fragment() == expected_fragment