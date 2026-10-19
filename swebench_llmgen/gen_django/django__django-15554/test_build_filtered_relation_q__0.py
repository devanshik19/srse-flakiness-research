import pytest
from django.db.models import Q
from django.db.models.sql.query import Query
from django.db.models.sql.where import WhereNode
from django.db.models.expressions import F

def test_build_filtered_relation_q():
    # Setup
    q_object = Q(name='test') & Q(age=30)
    query = Query(model=None)  # passing None since it won't be used directly

    # Test building without negation
    result = query.build_filtered_relation_q(q_object, reuse=False)
    assert isinstance(result, WhereNode)
    assert result.connector == 'AND'
    assert not result.negated
    assert len(result.children) == 2  # Two conditions in the Q object

    # Test building with negation
    q_object_negated = Q(name='test', negated=True) & Q(age=30, negated=False)
    result_negated = query.build_filtered_relation_q(q_object_negated, reuse=False)
    assert result_negated.negated
    assert len(result_negated.children) == 2
    assert result_negated.children[0].negated
    assert not result_negated.children[1].negated

    # Test with deeper nested conditions
    nested_q_object = Q(Q(name='test') | Q(name='demo')) & Q(age=30)
    result_nested = query.build_filtered_relation_q(nested_q_object, reuse=False)
    assert isinstance(result_nested, WhereNode)
    assert len(result_nested.children) == 3  # 2 from OR and 1 from AND

    # Verify the children connections
    assert result_nested.children[0].children[0].lhs == 'name'
    assert result_nested.children[0].children[1].lhs == 'name'
    assert result_nested.children[1].lhs == 'age'

    # Test building with allowed joins
    test_relation = query.build_filtered_relation_q(Q(F('profile__status') == 'active'), reuse=False)
    assert isinstance(test_relation, WhereNode)
    assert len(test_relation.children) == 1
    assert test_relation.children[0].lhs == 'profile__status'
    
    # Additional branches could be tested here with more complex Q objects