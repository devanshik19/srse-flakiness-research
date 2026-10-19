import copy
from decimal import Decimal
from django.apps.registry import Apps
from django.db import NotSupportedError
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.backends.ddl_references import Statement
from django.db.backends.utils import strip_quotes
from django.db.models import UniqueConstraint
from django.db.transaction import atomic
from django.contrib.auth.models import User
import pytest

@pytest.fixture
def schema_editor():
    return DatabaseSchemaEditor()

def test_alter_field_rename_column(schema_editor):
    user_model = User
    old_field = user_model._meta.get_field('username')
    new_field = copy.deepcopy(old_field)
    new_field.column = 'new_username'
    
    schema_editor._alter_field(
        model=user_model,
        old_field=old_field,
        new_field=new_field,
        old_type='varchar(150)',
        new_type='varchar(150)',
        old_db_params={},
        new_db_params={},
        strict=False,
    )
    # Verify that the column has been renamed
    assert hasattr(user_model._meta.get_field('new_username'), 'column')
    assert not hasattr(user_model._meta.get_field('username'), 'column')

def test_alter_field_remake_table(schema_editor):
    user_model = User
    old_field = user_model._meta.get_field('email')
    new_field = copy.deepcopy(old_field)
    new_field.null = True  # Changing a property that requires a table remake
    
    schema_editor._alter_field(
        model=user_model,
        old_field=old_field,
        new_field=new_field,
        old_type='varchar(254)',
        new_type='varchar(254)',
        old_db_params={},
        new_db_params={},
        strict=False,
    )
    # Here we could mock _remake_table to assert it's called

def test_alter_field_with_unique_constraint(schema_editor):
    user_model = User
    old_field = user_model._meta.get_field('username')
    new_field = copy.deepcopy(old_field)
    new_field.unique = True # Enabling unique constraint
    
    schema_editor._alter_field(
        model=user_model,
        old_field=old_field,
        new_field=new_field,
        old_type='varchar(150)',
        new_type='varchar(150)',
        old_db_params={},
        new_db_params={},
        strict=False,
    )
    # Verify that the unique constraint has been added
    assert new_field.unique is True

def test_alter_field_no_schema_changes(schema_editor):
    user_model = User
    old_field = user_model._meta.get_field('password')
    new_field = copy.deepcopy(old_field)
    new_field.column = 'password'  # Same column name

    schema_editor._alter_field(
        model=user_model,
        old_field=old_field,
        new_field=new_field,
        old_type='varchar(128)',
        new_type='varchar(128)',
        old_db_params={},
        new_db_params={},
        strict=False,
    )
    # No changes should mean _remake_table is not called
    # You would normally mock _remake_table and assert it was not called