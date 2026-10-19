import pytest
from django.db.models import Q
from django.db.models.sql.where import WhereNode
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_build_filtered_relation_q():
    query = Query(User)

    # Create a simple Q object with conditions
    q_object = Q(username='testuser', is_active=True)

    # Test with default parameters
    result = query.build_filtered_relation_q(q_object, reuse=False)
    
    assert isinstance(result, WhereNode)
    assert len(result.children) == 2  # Should have two conditions (username & is_active)

    # Check if operators and negation are handled properly
    connector = q_object.connector
    assert result.connector == connector
    assert result.negated == False  # No negation in the Q object

    # Test with negated conditions
    q_object_negated = Q(username='testuser', is_active=False)
    result_negated = query.build_filtered_relation_q(q_object_negated, reuse=False)
    
    assert result_negated.negated == False  # Negated is False (since we're adding negated clauses)
    assert len(result_negated.children) == 2

    # Test branches with complex Q expressions
    complex_q_object = Q(Q(username='testuser') | Q(is_superuser=True))
    result_complex = query.build_filtered_relation_q(complex_q_object, reuse=False)
    
    assert isinstance(result_complex, WhereNode)
    assert result_complex.connector == complex_q_object.connector
    assert len(result_complex.children) == 2  # Should handle both branches

    # Verifying that negation flags apply correctly in branches
    complex_q_object_negated = Q(Q(username='testuser') | Q(is_active=False)).negate()
    result_complex_negated = query.build_filtered_relation_q(complex_q_object_negated, reuse=False)

    assert result_complex_negated.negated == True
    assert len(result_complex_negated.children) == 2