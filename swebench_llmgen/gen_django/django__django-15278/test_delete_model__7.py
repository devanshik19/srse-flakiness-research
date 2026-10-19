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

@pytest.mark.django_db
def test_delete_model_handle_autom2m():
    # Arrange
    user = User.objects.create(username='testuser')
    editor = DatabaseSchemaEditor(None)  # Assuming necessary arguments are None

    # Act
    editor.delete_model(User, handle_autom2m=True)

    # Assert
    assert not User.objects.filter(pk=user.pk).exists()

@pytest.mark.django_db
def test_delete_model_no_handle_autom2m():
    # Arrange
    user = User.objects.create(username='testuser')
    editor = DatabaseSchemaEditor(None)  # Assuming necessary arguments are None

    # Add deferred SQL statement to simulate behavior
    editor.deferred_sql.append(Statement("SELECT * FROM auth_user WHERE username='testuser'"))

    # Act
    editor.delete_model(User, handle_autom2m=False)

    # Assert
    assert not User.objects.filter(pk=user.pk).exists()
    assert len(editor.deferred_sql) == 0  # Check if deferred SQL for the deleted table is removed