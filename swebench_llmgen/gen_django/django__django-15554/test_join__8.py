import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query
from django.db.models.sql.datastructures import Join

@pytest.fixture
def query():
    # Create a new Query object
    model = User._meta.model
    return Query(model, alias_cols=None)

def test_join_no_reuse(query):
    join = Join(
        table_name='auth_user',
        parent_alias='user',
        table_alias='user_1',
        join_type=None,
        nullable=False
    )
    alias = query.join(join)
    assert alias == 'user_1'
    assert join.table_alias == 'user_1'
    assert query.alias_map[alias].equals(join)

def test_join_with_reuse(query):
    join = Join(
        table_name='auth_user',
        parent_alias='user',
        table_alias='user_1',
        join_type=None,
        nullable=False
    )
    query.alias_map['user_1'] = join
    reused_alias = query.join(join, reuse={'user_1'})
    assert reused_alias == 'user_1'

def test_join_reuse_finds_most_recent(query):
    join1 = Join(table_name='auth_user', parent_alias='user', table_alias='user_1', join_type=None, nullable=False)
    join2 = Join(table_name='auth_user', parent_alias='user', table_alias='user_2', join_type=None, nullable=False)

    # Simulate adding an alias to the alias_map
    query.alias_map['user_1'] = join1
    query.alias_map['user_2'] = join2

    # Join with no reuse; expects a new alias to be generated
    join3 = Join(table_name='auth_user', parent_alias='user', table_alias='user_3', join_type=None, nullable=False)
    new_alias = query.join(join3)
    assert new_alias not in query.alias_map
    assert query.alias_map[new_alias].equals(join3)

def test_join_nullable_query_type(query):
    join = Join(
        table_name='auth_user',
        parent_alias='user',
        table_alias='user_1',
        join_type=None,
        nullable=True
    )
    new_alias = query.join(join)
    assert join.join_type == 'LOUTER'
    assert new_alias in query.alias_map

def test_join_non_nullable_query_type(query):
    join = Join(
        table_name='auth_user',
        parent_alias='user',
        table_alias='user_1',
        join_type=None,
        nullable=False
    )
    query.alias_map['user_1'] = join
    new_alias = query.join(join)
    assert join.join_type == 'INNER'
    assert new_alias == 'user_1'