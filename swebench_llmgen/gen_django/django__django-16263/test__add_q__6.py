import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query
from django.db.models.sql.where import WhereNode

@pytest.mark.django_db
def test_add_q():
    # Create a Query object
    query = Query(User)

    # Create Q objects for testing
    q1 = Q(username='testuser1')
    q2 = Q(is_active=True)

    # Prepare used aliases
    used_aliases = {}

    # Call _add_q method
    target_clause, needed_inner = query._add_q(q1, used_aliases)

    # Assert that the target_clause is a WhereNode
    assert isinstance(target_clause, WhereNode)
    assert target_clause.connector == 'AND'
    
    # Test the addition of another Q object
    target_clause, needed_inner = query._add_q(q2, used_aliases)
    
    # Check if the where node contains the necessary filters
    assert len(target_clause.children) == 2  # Expecting two conditions
    conditions = [child.get_sql() for child in target_clause.children]
    
    assert any("username = 'testuser1'" in cond for cond in conditions)
    assert any("is_active = True" in cond for cond in conditions)

    # Test negation on branch
    q3 = Q(username='testuser2', negated=True)
    target_clause, needed_inner = query._add_q(q3, used_aliases)
    
    assert any("username != 'testuser2'" in cond for cond in target_clause.children[0].get_sql())
    assert target_clause.negated is True

    # Test handling of negation
    q4 = Q(username='testuser3', negated=False)
    target_clause, needed_inner = query._add_q(q4, used_aliases, branch_negated=True)
    
    assert target_clause.negated is False  # Confirm negation is properly managed

    # Test with empty Q object
    q5 = Q()
    target_clause, needed_inner = query._add_q(q5, used_aliases)
    
    assert len(target_clause.children) == 0  # Expecting no conditions added