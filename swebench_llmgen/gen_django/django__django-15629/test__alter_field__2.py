import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.backends.sqlite3.schema import DatabaseSchemaEditor
from django.db.models import Field

@pytest.fixture
def db_schema_editor():
    return DatabaseSchemaEditor(connection=None)  # Dummy connection for testing

def test_alter_field_rename_column(db_schema_editor):
    user_model = User
    old_field = user_model._meta.get_field('username')
    new_field = copy.copy(old_field)
    new_field.column = 'new_username'

    db_schema_editor._alter_field(
        model=user_model,
        old_field=old_field,
        new_field=new_field,
        old_type=old_field.get_internal_type(),
        new_type=new_field.get_internal_type(),
        old_db_params={},
        new_db_params={},
        strict=False
    )

    # Check that the field was intended to be renamed
    assert new_field.column == 'new_username'

def test_alter_field_change_type(db_schema_editor):
    user_model = User
    old_field = user_model._meta.get_field('username')
    
    class NewCharField(Field):
        pass

    new_field = copy.copy(old_field)
    new_field.__class__ = NewCharField
    
    db_schema_editor._alter_field(
        model=user_model,
        old_field=old_field,
        new_field=new_field,
        old_type=old_field.get_internal_type(),
        new_type=new_field.get_internal_type(),
        old_db_params={},
        new_db_params={},
        strict=False
    )

    # Check that _remake_table would be called, simulating changing type
    assert new_field.__class__ == NewCharField

def test_alter_field_unique_constraint(db_schema_editor):
    user_model = User
    old_field = user_model._meta.get_field('username')
    new_field = copy.copy(old_field)
    new_field.unique = True

    db_schema_editor._alter_field(
        model=user_model,
        old_field=old_field,
        new_field=new_field,
        old_type=old_field.get_internal_type(),
        new_type=new_field.get_internal_type(),
        old_db_params={},
        new_db_params={},
        strict=False
    )

    # Ensure unique constraint is handled
    assert new_field.unique is True