import pytest
from django.contrib.auth.models import User
from django.db import connections
from django.db.models.sql.query import Query
from django.db.models.sql.datastructures import Join

@pytest.fixture
def setup_query():
    user_model = User._meta.object_name
    return Query(model=user_model, alias_cols=[])

def test_join_no_reuse(setup_query):
    query = setup_query
    join = Join(table_name='auth_user', parent_alias='user', join_type='INNER', nullable=False)

    alias = query.join(join)
    assert alias in query.alias_map  # Ensure alias is registered
    assert query.alias_map[alias].table_name == join.table_name  # Check table name matches

def test_join_with_reuse(setup_query):
    query = setup_query
    join = Join(table_name='auth_user', parent_alias='user', join_type='INNER', nullable=False)
    reuse_alias = query.join(join)  # first join

    join_2 = Join(table_name='auth_user', parent_alias='user', join_type='INNER', nullable=False)
    alias_2 = query.join(join_2, reuse={reuse_alias})  # second join with reuse

    assert alias_2 == reuse_alias  # Ensure reused alias is returned
    assert query.alias_map[alias_2].table_name == join_2.table_name  # Check table name matches

def test_join_nullable(setup_query):
    query = setup_query
    join = Join(table_name='auth_user', parent_alias='user', join_type='INNER', nullable=True)

    alias = query.join(join)
    assert alias in query.alias_map  # Ensure alias is registered
    assert query.alias_map[alias].join_type == 'LOUTER'  # Check join type is LOUTER due to nullable

def test_join_multiple_times(setup_query):
    query = setup_query
    join = Join(table_name='auth_user', parent_alias='user', join_type='INNER', nullable=False)

    alias_1 = query.join(join)  # first join
    alias_2 = query.join(join)  # second join (same join instance)

    assert alias_2 != alias_1  # Different aliases should be created
    assert query.alias_map[alias_1].table_alias == alias_1  # Check alias registration

def test_join_reuse_most_recent_alias(setup_query):
    query = setup_query
    join_1 = Join(table_name='auth_user', parent_alias='user', join_type='INNER', nullable=False)
    alias_1 = query.join(join_1)

    join_2 = Join(table_name='auth_user', parent_alias='user', join_type='INNER', nullable=False)
    alias_2 = query.join(join_2)

    # Now we try to reuse the previous join
    join_3 = Join(table_name='auth_user', parent_alias='user', join_type='INNER', nullable=False)
    reuse_alias = query.join(join_3, reuse={alias_2})

    assert reuse_alias == alias_2  # Ensure it reuses the most recent alias