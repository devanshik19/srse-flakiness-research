import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query


def test_join_with_reuse():
    query = Query(User)
    join = query.base_table_class(User._meta.db_table, None, None)

    # First call to join should create a new alias
    alias1 = query.join(join)
    assert alias1 in query.alias_map

    # Reuse this alias
    reuse_alias = {alias1}
    alias2 = query.join(join, reuse=reuse_alias)
    assert alias2 == alias1  # Should reuse the alias

    # Add another join that is not being reused
    new_join = query.base_table_class(User._meta.db_table, None, None)
    alias3 = query.join(new_join)
    assert alias3 not in reuse_alias  # Should be a new alias


def test_join_with_nullable_column():
    query = Query(User)
    join = query.base_table_class(User._meta.db_table, None, None)
    join.nullable = True

    # Create the first join
    alias1 = query.join(join)
    assert alias1 in query.alias_map
    assert query.alias_map[alias1].join_type == query.sql.constants.LOUTER

    # Create another join with non-nullable
    new_join = query.base_table_class(User._meta.db_table, None, None)
    new_join.nullable = False
    alias2 = query.join(new_join)
    assert query.alias_map[alias2].join_type == query.sql.constants.INNER


def test_join_without_reuse():
    query = Query(User)
    join = query.base_table_class(User._meta.db_table, None, None)

    # First call to join without reuse
    alias1 = query.join(join)
    assert alias1 in query.alias_map

    # Call join with different join
    another_join = query.base_table_class(User._meta.db_table, None, None)
    alias2 = query.join(another_join)
    assert alias2 not in {alias1}  # Different join should create a new alias

    # Verify they have different aliases
    assert alias1 != alias2


def test_join_edge_cases():
    query = Query(User)
    join = query.base_table_class(User._meta.db_table, None, None)

    # Join with no reuse and ensure it creates an alias
    first_alias = query.join(join)
    assert first_alias in query.alias_map

    # Attempt to reuse with an empty set
    new_alias = query.join(join, reuse=set())
    assert new_alias != first_alias  # Should create a new alias
    
    # Check the state of the alias map
    assert len(query.alias_map) == 2
    
    # Testing with a filter
    user_filter = Q(username='testuser')
    assert not query.has_filters()  # Initially no filters
    query.add_q(user_filter)  # Now add a filter
    assert query.has_filters()  # Should be true now