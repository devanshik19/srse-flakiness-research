import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_change_aliases():
    # Create dummy Query instance
    query = Query(model=User)

    # Setup initial state
    query.select = (query.get_external_cols(),)
    query.group_by = (query.get_external_cols(),)
    query.where = query.build_where(None)
    query.alias_map = {'old_alias': query.table_alias('auth_user', True, False)}
    query.alias_refcount = {'old_alias': 1}
    query.table_map = {query.alias_map['old_alias'].table_name: ['old_alias']}
    query.external_aliases = {'old_alias': False}
    
    # Define change map
    change_map = {'old_alias': 'new_alias'}

    # Perform change aliases
    query.change_aliases(change_map)

    # Assert select columns are relabeled
    assert query.select[0].alias == 'new_alias'
    
    # Assert group_by columns are relabeled
    assert query.group_by[0].alias == 'new_alias'
    
    # Assert where clause aliases are relabeled
    assert query.where.alias == 'new_alias'
    
    # Assert alias_map updated correctly
    assert 'new_alias' in query.alias_map
    assert 'old_alias' not in query.alias_map
    
    # Assert alias_refcount updated correctly
    assert 'new_alias' in query.alias_refcount
    assert 'old_alias' not in query.alias_refcount
    
    # Assert table_map updated correctly
    assert query.table_map[query.alias_map['new_alias'].table_name] == ['new_alias']
    
    # Assert external_aliases updated correctly
    assert query.external_aliases['new_alias'] == True
    assert 'old_alias' not in query.external_aliases