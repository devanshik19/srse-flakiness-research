import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query
from django.db.models.sql.datastructures import Join

@pytest.fixture
def query_instance():
    # Create a default Query instance 
    query = Query(User, [])
    return query

def test_join_reuses_alias(query_instance):
    join = Join('auth_user', 'user', 'INNER', 'dummy_alias')
    query_instance.alias_map = {'dummy_alias': join}
    
    # Test reusing an existing alias
    reuse_set = {'dummy_alias'}
    result_alias = query_instance.join(join, reuse=reuse_set)
    
    assert result_alias == 'dummy_alias'
    assert query_instance.ref_alias(join.table_alias)

def test_join_creates_new_alias(query_instance):
    join = Join('auth_user', 'user', 'INNER', None)
    query_instance.alias_map = {}

    # Test creating a new alias since none exists
    result_alias = query_instance.join(join)

    assert result_alias != join.table_alias
    assert join.table_alias == result_alias
    assert join.join_type == 'INNER'

def test_join_creates_louter_alias_when_nullable(query_instance):
    join = Join('auth_user', 'user', None, None)
    join.nullable = True
    query_instance.alias_map = {}

    # Test creating a new LOUTER alias due to nullable join
    result_alias = query_instance.join(join)

    assert result_alias != join.table_alias
    assert join.table_alias == result_alias
    assert join.join_type == 'LOUTER'

def test_join_respects_louter_condition(query_instance):
    parent_join = Join('auth_user', 'user', 'LOUTER', 'parent_alias')
    query_instance.alias_map = {'parent_alias': parent_join}
    
    join = Join('auth_user', 'user', None, None)
    join.nullable = False
    
    # LOUTER condition should be respected, so this should result in LOUTER
    query_instance.alias_map['parent_alias'].join_type = 'LOUTER'

    result_alias = query_instance.join(join)

    assert join.join_type == 'LOUTER'
    assert result_alias != join.table_alias
    assert join.table_alias == result_alias