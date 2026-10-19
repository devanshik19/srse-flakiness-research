import pytest
from django.db.models import Q
from django.db.models.sql.query import Query
from django.contrib.auth.models import User


def test_add_q():
    # Setup
    query = Query(model=User, alias_cols={})
    user_filter_q = Q(username='testuser')
    
    used_aliases = set()
    
    # Add Q object with no branches negated
    target_clause, needed_inner = query._add_q(
        q_object=user_filter_q,
        used_aliases=used_aliases,
        branch_negated=False,
        current_negated=False,
        allow_joins=True,
        split_subq=True,
        check_filterable=True
    )
    
    # Expected clauses and conditions
    assert target_clause.connector == 'AND'
    assert len(target_clause.children) == 1
    
    # Check the child clause's content
    child_clause = target_clause.children[0]
    assert child_clause == query.build_filter(user_filter_q.children[0], can_reuse=used_aliases)[0]
    
    # Test adding a negated Q object
    negated_q = Q(username='testuser', negated=True)
    target_clause, needed_inner = query._add_q(
        q_object=negated_q,
        used_aliases=used_aliases,
        branch_negated=False,
        current_negated=False,
        allow_joins=True,
        split_subq=True,
        check_filterable=True
    )
    
    assert target_clause.connector == 'AND'
    assert target_clause.negated is False
    assert len(target_clause.children) == 1

    negated_child_clause = target_clause.children[0]
    assert negated_child_clause.negated is True
    assert negated_child_clause == query.build_filter(negated_q.children[0], can_reuse=used_aliases)[0]