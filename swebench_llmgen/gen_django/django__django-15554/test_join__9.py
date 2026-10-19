import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query
from django.db.models.sql.datastructures import Join

def test_join_reuses_alias():
    query = Query(User)
    join = Join(User, User._meta.db_table, LOUTER)
    query.alias_map = { 'user_alias': join }

    # Reuse existing alias
    reused_alias = query.join(join, reuse={'user_alias'})
    assert reused_alias == 'user_alias'
    assert join.join_type == LOUTER

def test_join_creates_new_alias():
    query = Query(User)
    join = Join(User, User._meta.db_table, INNER)
    query.alias_map = {}

    # Create new alias
    new_alias = query.join(join)
    assert new_alias in query.alias_map
    assert query.alias_map[new_alias] == join
    assert join.join_type == INNER

def test_join_nullable():
    query = Query(User)
    join = Join(User, User._meta.db_table, None, nullable=True)
    query.alias_map = { 'other_alias': Join(User, User._meta.db_table) }

    # Should create LOUTER join
    new_alias = query.join(join)
    assert query.alias_map[new_alias] == join
    assert join.join_type == LOUTER

def test_join_reuses_latest_alias():
    query = Query(User)
    first_join = Join(User, User._meta.db_table, INNER)
    second_join = Join(User, User._meta.db_table, LOUTER)
    query.alias_map = {
        'first_alias': first_join,
        'latest_alias': second_join
    }

    # Reusing the latest alias
    reused_alias = query.join(second_join, reuse={'first_alias', 'latest_alias'})
    assert reused_alias == 'latest_alias'
    
def test_join_with_no_reuse():
    query = Query(User)
    join = Join(User, User._meta.db_table, INNER)
    query.alias_map = {}

    # No reuse
    new_alias = query.join(join, reuse=set())
    assert new_alias in query.alias_map
    assert query.alias_map[new_alias] == join
    assert join.join_type == INNER