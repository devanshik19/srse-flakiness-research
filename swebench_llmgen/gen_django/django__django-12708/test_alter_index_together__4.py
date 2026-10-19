import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

@pytest.fixture
def schema_editor():
    return BaseDatabaseSchemaEditor(connection)

def test_alter_index_together_create_index(schema_editor):
    user_model = User
    old_index_together = [["first_name", "last_name"]]
    new_index_together = [["first_name", "last_name"], ["email"]]
    
    # Initial creation of the index
    schema_editor.alter_index_together(user_model, old_index_together, new_index_together)
    
    indexes = schema_editor._model_indexes_sql(user_model)
    assert any("first_name_idx" in index for index in indexes)
    assert any("email_idx" in index for index in indexes)

def test_alter_index_together_remove_index(schema_editor):
    user_model = User
    old_index_together = [["first_name", "last_name"], ["email"]]
    new_index_together = [["first_name", "last_name"]]
    
    # Initial creation of indexes
    schema_editor.alter_index_together(user_model, old_index_together, new_index_together)
    
    indexes = schema_editor._model_indexes_sql(user_model)
    assert any("email_idx" not in index for index in indexes)

def test_alter_index_together_no_change(schema_editor):
    user_model = User
    old_index_together = [["first_name", "last_name"]]
    new_index_together = [["first_name", "last_name"]]
    
    # No change in index
    schema_editor.alter_index_together(user_model, old_index_together, new_index_together)
    
    indexes = schema_editor._model_indexes_sql(user_model)
    assert any("first_name_idx" in index for index in indexes)
    assert len(indexes) == 1  # Only the existing index should remain