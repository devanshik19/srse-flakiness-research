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
def user_model():
    return User.objects.create(username='testuser', password='password')


def test_delete_model_handles_autom2m(user_model):
    editor = DatabaseSchemaEditor()

    # Ensure the user exists
    assert User.objects.filter(id=user_model.id).exists()

    # Call delete_model with handle_autom2m=True
    editor.delete_model(User, handle_autom2m=True)

    # Ensure the user is deleted
    assert not User.objects.filter(id=user_model.id).exists()


def test_delete_model_without_autom2m(user_model):
    editor = DatabaseSchemaEditor()

    # Ensure the user exists
    assert User.objects.filter(id=user_model.id).exists()

    # Create a deferred SQL statement referencing the user model
    statement = Statement("SELECT * FROM auth_user WHERE id = %s")
    editor.deferred_sql.append(statement)

    # Call delete_model with handle_autom2m=False
    editor.delete_model(User, handle_autom2m=False)

    # Ensure the user is deleted
    assert not User.objects.filter(id=user_model.id).exists()

    # Ensure the deferred statement referencing the user model is removed
    assert len(editor.deferred_sql) == 0