import operator
from functools import reduce
from django.core.exceptions import EmptyResultSet, FullResultSet
from django.db.models.expressions import Case, When
from django.db.models.lookups import Exact
from django.utils import tree
from django.utils.functional import cached_property
from django.db.models.sql.where import WhereNode

def test_replace_expressions():
    # Create mock WhereNode instances with a simple structure
    child_node_1 = WhereNode()
    child_node_2 = WhereNode()
    
    # Set up a WhereNode with children
    original_node = WhereNode()
    original_node.children = [child_node_1, child_node_2]
    original_node.connector = 'AND'
    original_node.negated = False
    
    # Create a replacements dictionary
    replacements = {
        original_node: WhereNode(),
        child_node_1: WhereNode(),
    }
    
    # Call the replace_expressions method
    new_node = original_node.replace_expressions(replacements)
    
    # Assertions to check if replacement happened correctly
    assert new_node is not original_node  # Ensure the clone is a different instance
    assert new_node.children[0] is replacements[child_node_1]  # Check child_node_1 was replaced
    assert new_node.children[1] is child_node_2  # child_node_2 should not have been replaced
    assert new_node.connector == original_node.connector  # connector should remain the same
    assert new_node.negated == original_node.negated  # negated should remain the same