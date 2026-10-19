import copy
from decimal import Decimal
from django.apps.registry import Apps
from django.db import NotSupportedError
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.backends.ddl_references import Statement
from django.db.backends.utils import strip_quotes
from django.db.models import UniqueConstraint, CharField, IntegerField
from django.db.transaction import atomic
from django.contrib.auth.models import User
import pytest

@pytest.mark.parametrize(
    "old_field, new_field, old_type, new_type, expected_execute_call",
    [
        # rename column without constraints
        (User._meta.get_field('username'), CharField(max_length=150, db_column='user_name'), str, str, True),
        # change type with constraints
        (User._meta.get_field('username'), CharField(max_length=200, db_column='username'), str, str, False),
        # unique constraint alteration
        (User._meta.get_field('email'), CharField(max_length=200, unique=True), str, str, True),
    ]
)
def test_alter_field(old_field, new_field, old_type, new_type, expected_execute_call):
    # Setup the DatabaseSchemaEditor
    editor = DatabaseSchemaEditor()

    # Call _alter_field function
    if expected_execute_call:
        with pytest.raises(NotSupportedError):
            editor._alter_field(User, old_field, new_field, old_type, new_type, {}, {}, strict=False)
    else:
        editor._alter_field(User, old_field, new_field, old_type, new_type, {}, {}, strict=False)
        # Add assertions based on expectation of internal state or side effects
        assert editor._remake_table.called