import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query
from django.db.models.sql.datastructures import Join

def test_join_reuse_existing_alias():
    query = Query(User)
    join = Join(User, alias='user_alias', join_type='INNER', nullable=True)
    
    # First join should create a new alias
    new_alias = query.join(join)
    assert new_alias == 'user_alias'  # Expect the alias to be the same
    
    # Reuse the alias
    reused_alias = query.join(join, reuse={new_alias})
    assert reused_alias == new_alias  # Expect to reuse the existing alias

def test_join_new_alias():
    query = Query(User)
    join1 = Join(User, alias='user_alias_1', join_type='INNER', nullable=False)
    join2 = Join(User, alias='user_alias_2', join_type='INNER', nullable=False)

    # First join should create a new alias
    alias1 = query.join(join1)
    assert alias1 == 'user_alias_1'

    # Second join should create a new alias since reuse set is empty
    alias2 = query.join(join2)
    assert alias2 == 'user_alias_2'

def test_join_with_nullable():
    query = Query(User)
    join = Join(User, alias='user_alias', join_type='INNER', nullable=True)

    # First join creates a new alias
    alias = query.join(join)
    assert alias == 'user_alias'  # Expect the alias to be 'user_alias'

    # Check join type updates correctly for nullable join
    assert join.join_type == 'LOUTER'  # Should change to LOUTER since it's nullable

def test_join_with_reuse_none():
    query = Query(User)
    join = Join(User, alias='user_alias', join_type=None, nullable=True)

    # Should create a new alias
    new_alias = query.join(join)
    assert new_alias == 'user_alias'

    # Reuse set is None, should create a new alias again
    join_again = Join(User, alias='user_alias', join_type=None, nullable=False)
    reused_alias = query.join(join_again, reuse=None)
    assert reused_alias != new_alias  # Expect to create a new alias

def test_join_with_existing_alias():
    query = Query(User)
    join1 = Join(User, alias='user_alias', join_type='INNER', nullable=False)
    join2 = Join(User, alias='user_alias', join_type='INNER', nullable=False)

    # Create the first join
    first_alias = query.join(join1)
    assert first_alias == 'user_alias'

    # Attempt to reuse the alias for a second join
    reused_alias = query.join(join2, reuse={first_alias})
    assert reused_alias == first_alias  # Expect to reuse the existing alias