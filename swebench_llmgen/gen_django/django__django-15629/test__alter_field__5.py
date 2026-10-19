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

class TestDatabaseSchemaEditor:
    @pytest.fixture
    def schema_editor(self):
        return DatabaseSchemaEditor()

    @pytest.fixture
    def user_model(self):
        return User

    def test_alter_field_rename_column(self, schema_editor, user_model):
        old_field = user_model._meta.get_field('username')
        new_field = copy.deepcopy(old_field)
        new_field.column = 'new_username'

        assert schema_editor._alter_field(
            user_model,
            old_field=old_field,
            new_field=new_field,
            old_type='varchar',
            new_type='varchar',
            old_db_params={},
            new_db_params={},
            strict=False
        ) is not None  # Expect it to execute a rename

    def test_alter_field_remake_table(self, schema_editor, user_model):
        old_field = user_model._meta.get_field('email')
        new_field = copy.deepcopy(old_field)
        new_field.blank = False  # Change a property to force table remake

        with pytest.raises(NotSupportedError):
            schema_editor._alter_field(
                user_model,
                old_field=old_field,
                new_field=new_field,
                old_type='varchar',
                new_type='varchar',
                old_db_params={},
                new_db_params={},
                strict=False
            )

    def test_alter_field_unique_constraint(self, schema_editor, user_model):
        old_field = user_model._meta.get_field('username')
        new_field = copy.deepcopy(old_field)
        new_field.unique = True

        assert schema_editor._alter_field(
            user_model,
            old_field=old_field,
            new_field=new_field,
            old_type='varchar',
            new_type='varchar',
            old_db_params={},
            new_db_params={},
            strict=False
        ) is not None  # Expect it to execute a remake and potentially a unique constraint update