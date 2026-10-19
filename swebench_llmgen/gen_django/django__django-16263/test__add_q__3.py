import pytest
from django.db.models import Q
from django.db.models.sql.query import Query
from django.contrib.auth.models import User
from django.db.models.sql.where import WhereNode

def test_add_q():
    query = Query(User)  # Create a query for the User model
    used_aliases = set()  # No used aliases initially
    q_object = Q(username='testuser')  # Create a simple Q object

    target_clause, needed_inner = query._add_q(q_object, used_aliases)

    assert isinstance(target_clause, WhereNode)  # Check if target clause is a WhereNode
    assert target_clause.connector == 'AND'      # Check the connector of the target clause
    assert len(target_clause.children) == 1      # Check it has one child (the Q object)

    child_clause = target_clause.children[0]
    assert child_clause.negated is False          # Check child's negation state
    assert child_clause.__str__() == "(`auth_user`.`username` = 'testuser')"  # Check expected SQL

    # Test with negation
    negated_q_object = Q(username='testuser', negated=True)
    target_clause_neg, needed_inner_neg = query._add_q(negated_q_object, used_aliases)

    assert len(target_clause_neg.children) == 1
    negated_child_clause = target_clause_neg.children[0]
    assert negated_child_clause.negated is True    # Check child's negation state after negation

    # Test with multiple conditions
    multi_q_object = Q(Q(username='testuser') | Q(is_staff=True))
    target_clause_multi, needed_inner_multi = query._add_q(multi_q_object, used_aliases)

    assert len(target_clause_multi.children) == 2    # Expect two children from OR condition
    assert target_clause_multi.connector == 'OR'      # Check if the connector is OR