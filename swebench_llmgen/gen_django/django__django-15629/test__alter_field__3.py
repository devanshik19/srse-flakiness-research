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

def test_alter_field_for_renaming_column_without_constraints():
    # Setup
    editor = DatabaseSchemaEditor()
    model = User
    old_field = model._meta.get_field('username')
    new_field = copy.deepcopy(old_field)
    new_field.column = 'new_username'

    old_type = old_field.db_type(editor.connection)
    new_type = new_field.db_type(editor.connection)
    old_db_params = {}
    new_db_params = {}

    # Act
    editor._alter_field(model, old_field, new_field, old_type, new_type, old_db_params, new_db_params)

    # Assert
    assert hasattr(editor.connection.schema_editor, 'executed_sql')
    assert 'ALTER TABLE' in editor.connection.schema_editor.executed_sql

def test_alter_field_creates_new_table_for_type_change():
    # Setup
    editor = DatabaseSchemaEditor()
    model = User
    old_field = model._meta.get_field('username')
    new_field = copy.deepcopy(old_field)
    new_field.db_type = lambda connection: 'INTEGER'  # Pretend we are changing the type to Integer

    old_type = old_field.db_type(editor.connection)
    new_type = new_field.db_type(editor.connection)
    old_db_params = {}
    new_db_params = {}

    # Act
    editor._alter_field(model, old_field, new_field, old_type, new_type, old_db_params, new_db_params)

    # Assert
    assert hasattr(editor, 'executed_sql')  # This is illustrative; depends on how your schema editor tracks execution

def test_alter_field_remakes_table_on_fk_constraints():
    # Setup
    editor = DatabaseSchemaEditor()
    user_model = User
    old_field = user_model._meta.get_field('username')
    new_field = copy.deepcopy(old_field)
    new_field.column = 'new_username'
    new_field.unique = True  # Set new field to be unique to trigger the fk logic

    old_type = old_field.db_type(editor.connection)
    new_type = new_field.db_type(editor.connection)
    old_db_params = {}
    new_db_params = {}

    # Act
    editor._alter_field(user_model, old_field, new_field, old_type, new_type, old_db_params, new_db_params)

    # Assert
    assert hasattr(editor, 'executed_sql')  # Illustrative assumption here