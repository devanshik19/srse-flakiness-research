import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

class TestBaseDatabaseSchemaEditor:

    @pytest.fixture
    def editor(self):
        return BaseDatabaseSchemaEditor(connection, collect_sql=False, atomic=False)

    @pytest.fixture
    def create_user_model(self, django_user_model):
        return django_user_model

    def test_alter_unique_together_addition(self, editor, create_user_model):
        # Initial unique_together constraint
        old_unique_together = {('username',)}
        new_unique_together = {('email',)}
        
        # Create the initial unique constraint
        editor.alter_unique_together(create_user_model, old_unique_together, old_unique_together)

        # Execute the change
        editor.alter_unique_together(create_user_model, old_unique_together, new_unique_together)

        # Assert the index change (check unique together added)
        indices = editor.connection.introspection.get_constraints(create_user_model._meta.db_table)
        assert ('email',) in indices

    def test_alter_unique_together_deletion(self, editor, create_user_model):
        # First set of constraints
        old_unique_together = {('username',)}
        new_unique_together = set()
        
        # Create the initial unique constraint
        editor.alter_unique_together(create_user_model, old_unique_together, old_unique_together)

        # Execute the change
        editor.alter_unique_together(create_user_model, old_unique_together, new_unique_together)

        # Assert unique together removed
        indices = editor.connection.introspection.get_constraints(create_user_model._meta.db_table)
        assert ('username',) not in indices