import pytest
from django.db.models import OuterRef, Subquery
from django.contrib.auth.models import User
from django.db.models.sql.constants import LOUTER
from django.db.models.sql.datastructures import BaseTable
from django.db.models.sql.where import WhereNode

@pytest.mark.parametrize("names_with_path, expected_trimmed_prefix, expected_contains_louter", [
    # Test with no m2m joins
    ([(None, []), (None, [BaseTable('auth_user', 'user')])], 
     ['user'], False),
    # Test with a m2m join and a left outer join present
    ([(None, []), (None, [BaseTable('auth_user', 'user')])], 
     ['user', 'friends'], True),
    # Test with multiple layers but trim to m2m join
    ([(None, []), (None, [BaseTable('auth_user', 'user')]), 
      (None, [BaseTable('auth_group', 'group')])],
     ['user'], False),
])

def test_trim_start(names_with_path, expected_trimmed_prefix, expected_contains_louter):
    query = Query(User, WhereNode())  # simulated initialized Query object
    query.alias_map = {f'user': BaseTable('auth_user', 'user'), 
                       f'group': BaseTable('auth_group', 'group')}
    query._lookup_joins = {'user'}
    query.base_table = 'user'
    query.unref_alias = lambda alias: None
    query.where_class = WhereNode
    query.set_select = lambda fields: None
    query.alias_refcount = {'user': 1, 'group': 1}

    # Manually set up mock joins
    for trimmed_paths, path in enumerate(names_with_path):
        path = base_path[path[0]]  # assign the expected table/lookup paths
    
    trimmed_prefix, contains_louter = query.trim_start(names_with_path)

    assert trimmed_prefix == expected_trimmed_prefix
    assert contains_louter == expected_contains_louter