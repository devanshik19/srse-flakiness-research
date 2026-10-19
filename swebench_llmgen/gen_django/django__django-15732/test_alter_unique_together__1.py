import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

class TestBaseDatabaseSchemaEditor:
    
    @pytest.fixture
    def schema_editor(self):
        return BaseDatabaseSchemaEditor(connection, collect_sql=False)

    def test_alter_unique_together_create_unique(self, schema_editor):
        # Set up initial unique_together
        User._meta.unique_together = {('username', 'email')}
        
        # Define the old and new unique_together
        old_unique_together = {('username', 'email')}
        new_unique_together = {('username', 'email'), ('first_name', 'last_name')}
        
        # Manually create fields for new unique_together
        User._meta.get_field('first_name')
        User._meta.get_field('last_name')
        
        # Execute the unique alteration
        schema_editor.alter_unique_together(User, old_unique_together, new_unique_together)
        
        # Check that the new unique_together has been added
        assert ('first_name', 'last_name') in User._meta.unique_together

    def test_alter_unique_together_remove_unique(self, schema_editor):
        # Set up initial unique_together
        User._meta.unique_together = {('username', 'email'), ('first_name', 'last_name')}
        
        # Define the old and new unique_together
        old_unique_together = {('username', 'email'), ('first_name', 'last_name')}
        new_unique_together = {('username', 'email')}
        
        # Execute the unique alteration
        schema_editor.alter_unique_together(User, old_unique_together, new_unique_together)
        
        # Check that the old unique_together has been removed
        assert ('first_name', 'last_name') not in User._meta.unique_together

    def test_alter_unique_together_no_change(self, schema_editor):
        # Set up initial unique_together
        User._meta.unique_together = {('username', 'email')}
        
        # Define the same unique_together
        old_unique_together = {('username', 'email')}
        new_unique_together = {('username', 'email')}
        
        # Execute the unique alteration (should not change anything)
        schema_editor.alter_unique_together(User, old_unique_together, new_unique_together)
        
        # Assert that unique_together remains unchanged
        assert User._meta.unique_together == {('username', 'email')}