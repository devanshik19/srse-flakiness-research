import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query
from django.db.models.sql.where import WhereNode
from django.db.models.sql.datastructures import BaseTable
from django.db.models import Q

def create_mock_query():
    query = Query(model=User, where=WhereNode(), aliases={})
    query.alias_map = {f'alias_{i}': BaseTable('auth_user', f'alias_{i}') for i in range(5)}
    query.alias_refcount = {alias: 1 for alias in query.alias_map}
    return query

def test_trim_start_no_m2m():
    query = create_mock_query()
    names_with_path = [
        ('user', [{'m2m': False, 'join_field': User._meta.get_field('username')}]),
        ('profile', [{'m2m': False, 'join_field': User._meta.get_field('email')}])
    ]
    trimmed_prefix, contains_louter = query.trim_start(names_with_path)
    assert trimmed_prefix == 'user.profile.email'
    assert contains_louter is False

def test_trim_start_with_m2m():
    query = create_mock_query()
    names_with_path = [
        ('group', [{'m2m': True, 'join_field': User._meta.get_field('groups')}]),
        ('user', [{'m2m': False, 'join_field': User._meta.get_field('username')}])
    ]
    trimmed_prefix, contains_louter = query.trim_start(names_with_path)
    assert trimmed_prefix == 'group'
    assert contains_louter is False

def test_trim_start_with_louter():
    query = create_mock_query()
    query.alias_map['alias_1'].join_type = 'LEFT OUTER JOIN'
    names_with_path = [
        ('group', [{'m2m': False, 'join_field': User._meta.get_field('groups')}]),
        ('user', [{'m2m': False, 'join_field': User._meta.get_field('username')}])
    ]
    trimmed_prefix, contains_louter = query.trim_start(names_with_path)
    assert trimmed_prefix == 'group'
    assert contains_louter is True