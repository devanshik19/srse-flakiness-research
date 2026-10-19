import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.backends.sqlite3.schema import DatabaseSchemaEditor

@pytest.mark.django_db
def test_alter_field_rename_column():
    editor = DatabaseSchemaEditor(connection=User.objects.model._meta.db_table)

    old_field = User._meta.get_field('username')
    new_field = models.CharField(max_length=150, db_column='user_name', default='')

    # Ensure the old field is present
    old_field.db_column = 'username'

    # Attempt to rename the column
    editor._alter_field(
        model=User,
        old_field=old_field,
        new_field=new_field,
        old_type=old_field.get_internal_type(),
        new_type=new_field.get_internal_type(),
        old_db_params={},
        new_db_params={},
    )

    # Confirm that the field has been renamed in the database
    assert not User._meta.get_field('username')  # Original field should not exist
    assert User._meta.get_field('user_name')  # New field should exist

def test_alter_field_remake_table():
    editor = DatabaseSchemaEditor(connection=User.objects.model._meta.db_table)

    old_field = User._meta.get_field('first_name')
    new_field = models.CharField(max_length=200)

    # Altering field type
    editor._alter_field(
        model=User,
        old_field=old_field,
        new_field=new_field,
        old_type=old_field.get_internal_type(),
        new_type=new_field.get_internal_type(),
        old_db_params={},
        new_db_params={},
    )

    # Confirm that the field type has been changed
    assert User._meta.get_field('first_name').max_length == 200

def test_alter_field_with_unique_constraint():
    editor = DatabaseSchemaEditor(connection=User.objects.model._meta.db_table)

    old_field = User._meta.get_field('email')
    new_field = models.EmailField(unique=True)

    # Ensure the old field is present and not unique
    old_field.unique = False

    # Attempt to alter field to change to unique
    editor._alter_field(
        model=User,
        old_field=old_field,
        new_field=new_field,
        old_type=old_field.get_internal_type(),
        new_type=new_field.get_internal_type(),
        old_db_params={},
        new_db_params={},
    )

    # Verify that the unique constraint is applied
    assert User._meta.get_field('email').unique is True