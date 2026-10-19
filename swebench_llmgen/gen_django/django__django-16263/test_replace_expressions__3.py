import pytest
from django.db.models.sql.where import WhereNode
from django.db.models import Q
from django.contrib.auth.models import User

def test_replace_expressions():
    # Setup for the test
    node1 = WhereNode()
    node2 = WhereNode()
    node3 = WhereNode()

    # Create mock children for the WhereNode instances
    node1.children = [node2]
    node2.children = [node3]
    
    # Define some replacements
    replacements = {
        node1: WhereNode(),
        node2: WhereNode(),
    }
    
    # Call replace_expressions on node1
    result = node1.replace_expressions(replacements)

    # Asserting the main node is replaced correctly
    assert isinstance(result, WhereNode)
    assert len(result.children) == 1

    # Asserting the first child has been replaced
    assert isinstance(result.children[0], WhereNode)

    # Check if the second child remains, which is not in the replacements
    assert len(result.children[0].children) == 1
    assert result.children[0].children[0] is node3

    # Test with no replacements
    result_no_replacements = node1.replace_expressions({})
    
    # Asserting that the original structure is retained
    assert result_no_replacements is not result
    assert result_no_replacements.children[0] is node2
    assert result_no_replacements.children[0].children[0] is node3