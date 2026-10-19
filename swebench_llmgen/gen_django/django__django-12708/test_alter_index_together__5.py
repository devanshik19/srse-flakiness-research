import pytest
from django.contrib.auth.models import User
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

def test_alter_index_together():
    editor = BaseDatabaseSchemaEditor(None, collect_sql=False)

    # Old index together
    old_index_together = [("first_name", "last_name")]
    # New index together includes a new index
    new_index_together = [("first_name", "last_name"), ("email",)]
    
    user_model = User

    # Simulating creating the old index
    editor.alter_index_together(user_model, old_index_together, new_index_together)
    
    # Check if old index is deleted and new index is created
    assert not editor._delete_composed_index_called
    assert editor._create_index_called

    # Reset the call counts
    editor._delete_composed_index_called = False
    editor._create_index_called = False

    # New situation with index changes : removing all indexes
    editor.alter_index_together(user_model, new_index_together, [])
    
    # Check that old indexes have been deleted
    assert editor._delete_composed_index_called
    assert not editor._create_index_called

    # Check thresholds for edges: 
    # 1. Assuming no changes
    editor.alter_index_together(user_model, [], [])
    assert not editor._delete_composed_index_called
    assert not editor._create_index_called

    # 2. Changing to different but unchanged
    editor.alter_index_together(user_model, [("email",)], [("email",)])
    assert not editor._delete_composed_index_called
    assert not editor._create_index_called