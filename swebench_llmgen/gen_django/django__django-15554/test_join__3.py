import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query
from django.db.models.sql.datastructures import Join


@pytest.fixture
def setup_query():
    user_model = User
    query = Query(user_model._meta)
    return query


def test_join_with_reuse(setup_query):
    query = setup_query
    join = Join('auth_user', 'user', 'INNER', alias='user_alias')
    
    # First join; should not reuse
    first_alias = query.join(join)
    assert first_alias == 'user_alias'
    assert 'user_alias' in query.alias_map

    # Reuse the join alias
    reused_alias = query.join(join, reuse={'user_alias'})
    assert reused_alias == 'user_alias'  # Reused the existing alias


def test_join_without_reuse(setup_query):
    query = setup_query
    join_1 = Join('auth_user', 'user_one', 'INNER', alias='user_one_alias')
    join_2 = Join('auth_user', 'user_two', 'INNER', alias='user_two_alias')

    # First join; should not reuse
    first_alias = query.join(join_1)
    assert first_alias == 'user_one_alias'
    assert 'user_one_alias' in query.alias_map

    # Second join; no reuse available
    second_alias = query.join(join_2)
    assert second_alias == 'user_two_alias'
    assert 'user_two_alias' in query.alias_map


def test_join_nullable(setup_query):
    query = setup_query
    join = Join('auth_user', 'user_nullable', 'LEFT OUTER', alias='nullable_user_alias', nullable=True)

    # Join with nullable flag; should create as LOUTER
    alias = query.join(join)
    assert alias == 'nullable_user_alias'
    assert query.alias_map[alias].join_type == 'LOUTER'


def test_join_with_louter_parent(setup_query):
    query = setup_query
    parent_join = Join('auth_user', 'parent_user', 'LEFT OUTER', alias='parent_user_alias')
    child_join = Join('auth_user', 'child_user', 'INNER', alias='child_user_alias')

    # Join parent first
    parent_alias = query.join(parent_join)
    assert parent_alias == 'parent_user_alias'
    
    # Join child; should be LOUTER due to parent being LOUTER
    child_alias = query.join(child_join)
    assert child_alias == 'child_user_alias'
    assert query.alias_map[child_alias].join_type == 'LOUTER'