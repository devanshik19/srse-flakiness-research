import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query
from django.db.models.sql.datastructures import Join

def test_join_reuses_alias():
    # Setup a Query instance
    query = Query(model=User, alias_cols=True)
    
    # Create a join instance
    join1 = Join(table_name='auth_user', parent_alias='1', nullable=False)
    alias1 = query.join(join1)

    # Reuse the alias
    join2 = Join(table_name='auth_user', parent_alias='1', nullable=False)
    alias2 = query.join(join2, reuse={alias1})

    assert alias1 == alias2, "The alias should be reused."

def test_join_creates_new_alias():
    # Setup a Query instance
    query = Query(model=User, alias_cols=True)

    # Create a join instance
    join1 = Join(table_name='auth_user', parent_alias='1', nullable=False)
    alias1 = query.join(join1)

    # Create a new join instance, marked as nullable
    join2 = Join(table_name='auth_user', parent_alias='1', nullable=True)
    alias2 = query.join(join2)

    assert alias1 != alias2, "A new alias should be created for a nullable join."

def test_join_reuses_most_recent_alias():
    # Setup a Query instance
    query = Query(model=User, alias_cols=True)

    # Create multiple joins and test reuse
    join1 = Join(table_name='auth_user', parent_alias='1', nullable=False)
    query.join(join1)

    join2 = Join(table_name='auth_user', parent_alias='1', nullable=False)
    query.join(join2)

    join3 = Join(table_name='auth_user', parent_alias='1', nullable=False)
    alias3 = query.join(join3, reuse={join1.table_alias, join2.table_alias})

    assert alias3 == join2.table_alias, "Should reuse the most recent alias."

def test_join_handles_louter():
    # Setup a Query instance
    query = Query(model=User, alias_cols=True)

    # Louter join test
    join1 = Join(table_name='auth_user', parent_alias='1', nullable=True)
    alias1 = query.join(join1)

    assert join1.join_type == 'LOUTER', "Join should be LOUTER due to nullable setting."