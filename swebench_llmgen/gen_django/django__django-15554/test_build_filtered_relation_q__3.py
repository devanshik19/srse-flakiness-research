import pytest
from django.db.models import Q
from django.db.models.sql.query import Query
from django.db.models.sql.where import WhereNode

def test_build_filtered_relation_q():
    # Setup
    q_object = Q(name='test') & Q(age__gt=20)
    query = Query(model=None)
    
    # Test for no negation
    result = query.build_filtered_relation_q(q_object, reuse=False)
    assert isinstance(result, WhereNode)
    assert result.connector == 'AND'
    assert not result.negated
    assert len(result.children) == 2  # there are two conditions in the Q object
    
    # Test for negated branch
    q_object_negated = ~q_object
    result_negated = query.build_filtered_relation_q(q_object_negated, reuse=False)
    assert isinstance(result_negated, WhereNode)
    assert result_negated.connector == 'AND'
    assert result_negated.negated
    assert len(result_negated.children) == 2

    # Test with reuse enabled
    re_use = True
    result_reuse = query.build_filtered_relation_q(q_object, reuse=re_use)
    assert isinstance(result_reuse, WhereNode)
    assert result_reuse.connector == 'AND'
    assert not result_reuse.negated
    assert len(result_reuse.children) == 2

    # Test branch negated
    result_branch_negated = query.build_filtered_relation_q(q_object, reuse=False, branch_negated=True)
    assert isinstance(result_branch_negated, WhereNode)
    assert result_branch_negated.connector == 'AND'
    assert result_branch_negated.negated
    assert len(result_branch_negated.children) == 2

    # Test current negated
    result_current_negated = query.build_filtered_relation_q(q_object, reuse=False, current_negated=True)
    assert isinstance(result_current_negated, WhereNode)
    assert result_current_negated.connector == 'AND'
    assert result_current_negated.negated
    assert len(result_current_negated.children) == 2