import pytest
from django.db.models import Q
from django.db.models.sql.query import Query
from django.contrib.auth.models import User

def test_add_q():
    query = Query(model=User, alias_cols=[])

    # Create Q objects for testing
    q1 = Q(username='testuser1')
    q2 = Q(is_active=True)
    negated_q = Q(username='testuser2', negated=True)

    # Test with a non-negated Q object
    result_clause, needed_inner = query._add_q(q1, used_aliases=[])
    assert result_clause.negated is False
    assert len(result_clause.children) == 1

    # Test with AND connector
    assert result_clause.connector == 'AND'
    assert result_clause.children[0].lhs == q1.children[0].lhs
    assert result_clause.children[0].rhs == q1.children[0].rhs

    # Test with a negated Q object
    result_clause, needed_inner = query._add_q(negated_q, used_aliases=[])
    assert result_clause.negated is True
    assert len(result_clause.children) == 1
    assert result_clause.children[0].lhs == negated_q.children[0].lhs
    assert result_clause.children[0].rhs == negated_q.children[0].rhs

    # Test with multiple Q objects
    combined_q = Q(q1 & q2)
    result_clause, needed_inner = query._add_q(combined_q, used_aliases=[])
    assert result_clause.negated is False
    assert len(result_clause.children) == 2  # Both Q objects should be added
    assert result_clause.children[0].lhs == q1.children[0].lhs
    assert result_clause.children[1].lhs == q2.children[0].lhs
    assert result_clause.connector == 'AND'  # The connector should still be AND