import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_change_aliases():
    # Create a mock Query object
    query = Query(User)

    # Initial aliases and their count
    query.alias_map = {
        'user_alias': query.base_table_class(model=User),
        'other_alias': query.base_table_class(model=User)
    }
    query.alias_refcount = {
        'user_alias': 1,
        'other_alias': 1
    }
    query.select = (query.base_table_class(model=User),)
    query.group_by = (query.base_table_class(model=User),)
    query.where = query.base_table_class(model=User)
    query.external_aliases = {
        'user_alias': False,
        'other_alias': False,
    }

    # Change map: old aliases to new aliases
    change_map = {
        'user_alias': 'new_user_alias',
        'other_alias': 'new_other_alias'
    }

    # Call the method under test
    query.change_aliases(change_map)

    # Assertions to ensure changes are applied correctly
    assert 'new_user_alias' in query.alias_map
    assert 'new_other_alias' in query.alias_map
    assert 'user_alias' not in query.alias_map
    assert 'other_alias' not in query.alias_map
    assert query.alias_refcount['new_user_alias'] == 1
    assert query.alias_refcount['new_other_alias'] == 1
    assert query.select[0].alias == 'new_user_alias'
    assert query.group_by[0].alias == 'new_user_alias'
    assert query.external_aliases['new_user_alias'] == True
    assert query.external_aliases['new_other_alias'] == True