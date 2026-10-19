import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query
from django.db.models.sql.datastructures import Join

@pytest.fixture
def setup_query():
    # Create a simple Query object
    user = User.objects.create(username='testuser')
    query = Query(model=User, alias_cols=None)
    return query, user

def test_join_with_reuse(setup_query):
    query, _ = setup_query

    # Create a join instance
    join = Join(table_name='auth_user', parent_alias='auth_user', join_type=None)
    
    # First join
    alias1 = query.join(join)
    assert alias1 in query.alias_map
    assert query.alias_map[alias1] == join

    # Reuse the join
    reuse_aliases = {alias1}
    alias2 = query.join(join, reuse=reuse_aliases)
    assert alias2 == alias1  # Should reuse the same alias
    assert query.alias_map[alias2] == join  # Ensure the join is still correct

def test_join_without_reuse(setup_query):
    query, _ = setup_query

    # Create a join instance
    join = Join(table_name='auth_user', parent_alias='auth_user', join_type=None)

    # First join
    alias1 = query.join(join)
    assert alias1 in query.alias_map

    # Create another join with a new alias
    join2 = Join(table_name='auth_user', parent_alias='auth_user', join_type=None)
    alias2 = query.join(join2)
    assert alias2 != alias1  # Should not reuse and create a new alias
    assert alias2 in query.alias_map
    assert query.alias_map[alias2] == join2  # Ensure the new join is correctly mapped

def test_join_with_nullable(setup_query):
    query, _ = setup_query

    # Create a nullable join instance
    join = Join(table_name='auth_user', parent_alias='auth_user', join_type=None, nullable=True)
    
    # Join will create as LOUTER
    alias = query.join(join)
    assert query.alias_map[alias].join_type == 'LOUTER'  # Must be LOUTER due to nullable

def test_join_with_inner_when_not_nullable(setup_query):
    query, _ = setup_query

    # Create a non-nullable join instance
    join = Join(table_name='auth_user', parent_alias='auth_user', join_type=None, nullable=False)

    # First join
    alias1 = query.join(join)
    assert query.alias_map[alias1].join_type == 'INNER'  # Should be INNER 

def test_join_with_none_reuse(setup_query):
    query, _ = setup_query
    
    # Create a join instance
    join = Join(table_name='auth_user', parent_alias='auth_user', join_type=None)

    # Join without any reuse
    alias1 = query.join(join)
    assert alias1 in query.alias_map

    # Create another join
    join2 = Join(table_name='auth_user', parent_alias='auth_user', join_type=None)
    alias2 = query.join(join2, reuse=None)

    assert alias2 != alias1  # Must create a new alias
    assert alias2 in query.alias_map