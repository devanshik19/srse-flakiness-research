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

def test_delete_model_with_handle_autom2m(schema_editor):
    User.objects.create(username='testuser')
    user_model = User

    # Pre-check: ensure the table exists
    assert user_model._meta.db_table in schema_editor.connection.introspection.table_names()

    # Call the focal function
    schema_editor.delete_model(user_model, handle_autom2m=True)

    # Post-check: ensure the table no longer exists
    assert user_model._meta.db_table not in schema_editor.connection.introspection.table_names()

def test_delete_model_without_handle_autom2m(schema_editor):
    User.objects.create(username='testuser')
    user_model = User

    # Pre-check: ensure the table exists
    assert user_model._meta.db_table in schema_editor.connection.introspection.table_names()

    # Call the focal function
    schema_editor.delete_model(user_model, handle_autom2m=False)

    # Post-check: ensure the table no longer exists
    assert user_model._meta.db_table not in schema_editor.connection.introspection.table_names()

    # Ensure deferred statements referencing the deleted table are removed
    statement = Statement("ALTER TABLE %s RENAME TO new_table_name" % user_model._meta.db_table)
    schema_editor.deferred_sql.append(statement)
    assert statement in schema_editor.deferred_sql

    # Run the delete_model again
    schema_editor.delete_model(user_model, handle_autom2m=False)

    # Post-check: ensure deferred statements referencing the table are removed
    assert statement not in schema_editor.deferred_sql