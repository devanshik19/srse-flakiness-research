import pytest
from django.db.models.sql.where import WhereNode
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_build_filtered_relation_q():
    query = Query(model=User, alias_cols=[])

    # Test case 1: Simple Q object with no negation or children
    q_object_1 = Q(is_active=True)
    result_1 = query.build_filtered_relation_q(q_object_1, reuse=False)
    expected_clause_1 = WhereNode(connector='AND', negated=False)
    expected_clause_1.add(query.build_filter('is_active', can_reuse=False, branch_negated=False, current_negated=False)[0], 'AND')
    assert str(result_1) == str(expected_clause_1)

    # Test case 2: Q object with negation
    q_object_2 = Q(is_active=False)
    result_2 = query.build_filtered_relation_q(q_object_2, reuse=False)
    expected_clause_2 = WhereNode(connector='AND', negated=True)
    expected_clause_2.add(query.build_filter('is_active', can_reuse=False, branch_negated=True, current_negated=False)[0], 'AND')
    assert str(result_2) == str(expected_clause_2)

    # Test case 3: Q object with multiple conditions
    q_object_3 = Q(is_active=True) | Q(is_staff=True)
    result_3 = query.build_filtered_relation_q(q_object_3, reuse=False)
    expected_clause_3 = WhereNode(connector='OR', negated=False)
    expected_clause_3.add(query.build_filter('is_active', can_reuse=False, branch_negated=False, current_negated=False)[0], 'OR')
    expected_clause_3.add(query.build_filter('is_staff', can_reuse=False, branch_negated=False, current_negated=False)[0], 'OR')
    assert str(result_3) == str(expected_clause_3)

    # Test case 4: Nested Q objects
    q_object_4 = Q(is_active=True) & Q(Q(is_staff=True) | Q(is_superuser=True))
    result_4 = query.build_filtered_relation_q(q_object_4, reuse=False)
    expected_clause_4 = WhereNode(connector='AND', negated=False)
    expected_clause_4.add(query.build_filter('is_active', can_reuse=False, branch_negated=False, current_negated=False)[0], 'AND')
    nested_clause = WhereNode(connector='OR', negated=False)
    nested_clause.add(query.build_filter('is_staff', can_reuse=False, branch_negated=False, current_negated=False)[0], 'OR')
    nested_clause.add(query.build_filter('is_superuser', can_reuse=False, branch_negated=False, current_negated=False)[0], 'OR')
    expected_clause_4.add(nested_clause, 'AND')
    assert str(result_4) == str(expected_clause_4)