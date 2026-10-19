import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

@pytest.fixture
def schema_editor():
    return BaseDatabaseSchemaEditor(connection)

def test_alter_index_together_create(schema_editor):
    user_model = User
    old_index_together = [['username', 'email']]
    new_index_together = [['username', 'email'], ['first_name', 'last_name']]
    
    # Execute the alter_index_together method
    schema_editor.alter_index_together(user_model, old_index_together, new_index_together)

    # Verify that the new index has been created
    new_indexes = schema_editor._model_indexes_sql(user_model)
    assert any('first_name' in idx and 'last_name' in idx for idx in new_indexes)
    
def test_alter_index_together_delete(schema_editor):
    user_model = User
    old_index_together = [['username', 'email'], ['first_name', 'last_name']]
    new_index_together = [['username', 'email']]
    
    # We need to create the index first for deletion to work
    schema_editor.alter_index_together(user_model, old_index_together, new_index_together)

    # Execute the alter_index_together method to delete an index
    schema_editor.alter_index_together(user_model, old_index_together, new_index_together)

    # Verify that the index has been deleted
    new_indexes = schema_editor._model_indexes_sql(user_model)
    assert not any('first_name' in idx and 'last_name' in idx for idx in new_indexes)
    
def test_alter_index_together_no_change(schema_editor):
    user_model = User
    old_index_together = [['username', 'email']]
    new_index_together = [['username', 'email']]
    
    # Execute the alter_index_together method with no changes
    schema_editor.alter_index_together(user_model, old_index_together, new_index_together)

    # Ensure no changes were made to the indexes
    new_indexes = schema_editor._model_indexes_sql(user_model)
    assert len(new_indexes) == 1  # Should still be the original index