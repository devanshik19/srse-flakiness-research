import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

class TestBaseDatabaseSchemaEditor:

    def setup_method(self):
        self.schema_editor = BaseDatabaseSchemaEditor(connection)

    def test_alter_unique_together_add(self):
        # Creating a model `User` with a unique constraint
        user_model = User
        old_unique_together = {('username',)}
        new_unique_together = {('username',), ('email',)}

        # Simulate django calling alter_unique_together
        self.schema_editor.alter_unique_together(user_model, old_unique_together, new_unique_together)

        # Fetching the unique constraints back to ensure it was added
        constraints = user_model._meta.constraints
        assert len(constraints) == 2  # Expecting username and email constraints

    def test_alter_unique_together_remove(self):
        # Assume we are starting with a model `User` already having email unique constraint
        user_model = User
        old_unique_together = {('username',), ('email',)}
        new_unique_together = {('username',)}

        # Simulate django calling alter_unique_together
        self.schema_editor.alter_unique_together(user_model, old_unique_together, new_unique_together)

        # Fetching the unique constraints back to ensure it was removed
        constraints = user_model._meta.constraints
        assert len(constraints) == 1  # Expecting only username remains

    def test_alter_unique_together_no_change(self):
        user_model = User
        old_unique_together = {('username',)}
        new_unique_together = {('username',)}

        # Even if we call it, there should be no effect
        self.schema_editor.alter_unique_together(user_model, old_unique_together, new_unique_together)

        # Fetching the unique constraints back to ensure it did not change
        constraints = user_model._meta.constraints
        assert len(constraints) == 1  # Should still be the same count
        assert ('username',) in [(c.fields) for c in constraints]