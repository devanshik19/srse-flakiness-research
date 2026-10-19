import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def setup_query():
    # Create a Query instance for testing
    user_model = User._meta.model
    query = Query(user_model, alias_cols=['id', 'username'])
    return query

def test_change_aliases_no_aliases(setup_query):
    query = setup_query
    
    # Set up initial state
    query.select = (query._get_col('username', User._meta.get_field('username')),)
    query.where = query.build_where(Q(username='testuser'))
    query.group_by = ('username',)
    query.alias_map = {'user': query.table_alias('auth_user', create=True, filtered_relation=False)}
    query.alias_refcount = {'user': 1}
    
    # Change map with no collisions
    change_map = {'user': 'new_user'}
    
    # Call the method
    query.change_aliases(change_map)
    
    # Assertions
    assert 'new_user' in query.alias_map
    assert 'user' not in query.alias_map
    assert query.alias_refcount['new_user'] == 1
    assert 'new_user' in query.external_aliases
    assert query.external_aliases['new_user'] is True

def test_change_aliases_with_collisions(setup_query):
    query = setup_query
    
    # Set initial state
    query.select = (query._get_col('username', User._meta.get_field('username')),)
    query.where = query.build_where(Q(username='testuser'))
    query.group_by = ('username',)

    # Create an initial alias to test collision
    query.alias_map = {'user': query.table_alias('auth_user', create=True, filtered_relation=False)}
    query.alias_refcount = {'user': 1, 'new_user': 1}
    
    # Change map causing a collision
    change_map = {'user': 'new_user'}  # This will conflict with existing alias

    # Call the method and check for proper handling (should ignore because of assert)
    query.change_aliases(change_map)

    # Assertions after supposed collision handling
    assert 'new_user' in query.alias_map
    assert 'user' not in query.alias_map
    assert query.alias_refcount['new_user'] == 1

def test_change_aliases_empty_map(setup_query):
    query = setup_query
    
    # Set initial state
    query.select = (query._get_col('username', User._meta.get_field('username')),)
    query.where = query.build_where(Q(username='testuser'))
    
    # Test with an empty change_map
    change_map = {}

    # Call the method
    query.change_aliases(change_map)
    
    # Assertions - nothing should change
    assert query.select == (query._get_col('username', User._meta.get_field('username')),)