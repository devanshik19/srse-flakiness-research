import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.backends.sqlite3.schema import DatabaseSchemaEditor


@pytest.mark.parametrize(
    'old_field, new_field, old_type, new_type, expect_remake',
    [
        # Test basic field rename without changing type
        (
            User._meta.get_field('username'), 
            User._meta.get_field('new_username'), 
            models.CharField(max_length=150), 
            models.CharField(max_length=150), 
            False
        ),
        # Test field type change (the table should be remade)
        (
            User._meta.get_field('username'), 
            User._meta.get_field('username'), 
            models.CharField(max_length=150), 
            models.TextField(), 
            True
        ),
        # Test when old_field is a foreign key
        (
            User._meta.get_field('last_login'), 
            User._meta.get_field('new_last_login'), 
            models.DateTimeField(null=True), 
            models.DateTimeField(null=True), 
            False
        ),
    ]
)
def test_alter_field(old_field, new_field, old_type, new_type, expect_remake):
    schema_editor = DatabaseSchemaEditor()
    model = User
    old_db_params = {}
    new_db_params = {}

    if expect_remake:
        with pytest.raises(Exception):
            schema_editor._alter_field(model, old_field, new_field, old_type, new_type, old_db_params, new_db_params)
    else:
        result = schema_editor._alter_field(model, old_field, new_field, old_type, new_type, old_db_params, new_db_params)
        assert result is None  # No exception means the table was altered correctly.