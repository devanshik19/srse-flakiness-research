import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_change_aliases():
    # Setup the initial Query object
    query = Query(model=User, alias_cols=['id', 'username'])
    
    # Define initial aliases
    query.alias_map = {
        'old_alias': query.base_table_class('old_table'),  # Mocking a table class with a simple str name
    }
    query.alias_refcount = {
        'old_alias': 1,
    }
    query.table_map = {
        'old_table': ['old_alias']
    }
    query.select = (User._meta.get_field('id').column,)
    query.where = query.get_compiler(None).where
    query.group_by = (User._meta.get_field('id').column,)
    query.annotations = {}

    # Change map
    change_map = {
        'old_alias': 'new_alias',
    }

    # Call the function to test
    query.change_aliases(change_map)

    # Validate that the aliases were changed properly
    assert 'new_alias' in query.alias_map
    assert 'old_alias' not in query.alias_map
    assert 'old_alias' not in query.alias_refcount
    assert 'new_alias' in query.alias_refcount
    assert query.table_map['old_table'] == ['new_alias']
    
    # Validate that the select and group by columns were relabeled
    assert query.select == (User._meta.get_field('id').column,)
    assert query.group_by == (User._meta.get_field('id').column,)
    
    # Validate external aliases
    assert query.external_aliases.get('new_alias', False) is True