import pytest
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_add_q():
    # Create a Query instance with a sample model
    query = Query(User)

    # Create a sample Q object for testing
    q_object = Q(username='test_user') & Q(is_active=True)

    # Prepare variables for the function call
    used_aliases = set()
    
    # Call the _add_q function
    target_clause, needed_inner = query._add_q(
        q_object=q_object,
        used_aliases=used_aliases,
        branch_negated=False,
        current_negated=False,
        allow_joins=True,
        split_subq=True,
        check_filterable=True,
    )

    # Check properties of the resulting target_clause
    assert isinstance(target_clause, WhereNode)
    assert target_clause.connector == AND

    # Check if children were added correctly
    assert len(target_clause.children) == 2  # Two conditions in q_object

    # Validate the needed_inner output
    assert isinstance(needed_inner, bool)