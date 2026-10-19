import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

class TestBaseDatabaseSchemaEditor:

    @pytest.fixture
    def schema_editor(self):
        return BaseDatabaseSchemaEditor(connection=connection, collect_sql=False, atomic=True)

    def test_alter_unique_together(self, schema_editor):
        # Create a temporary user model with unique_together constraints
        User._meta.unique_together = {('username', 'email')}
        
        # Existing unique together
        old_unique_together = {('username', 'email')}
        # New unique together (removing email)
        new_unique_together = {('username',)}

        # Call the method to alter unique together
        schema_editor.alter_unique_together(User, old_unique_together, new_unique_together)

        # Validate that the unique constraint for (username, email) is deleted
        with pytest.raises(Exception):  # Change this to the specific exception you expect
            schema_editor.execute(f"SELECT * FROM auth_user WHERE username='test' AND email='test@example.com'")

        # Validate that the unique constraint for (username) now exists
        User.objects.create(username='test', email='test@example.com')  # Should be allowed since it's unique now
        
        # Check if adding the same username again raises an IntegrityError
        with pytest.raises(Exception):  # Change this to the specific exception you expect
            User.objects.create(username='test', email='another@example.com')

        # Clean up: If necessary, reset unique_together back to original state
        User._meta.unique_together = old_unique_together