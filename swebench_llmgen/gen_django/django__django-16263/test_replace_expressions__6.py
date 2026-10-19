import operator
from functools import reduce
from django.core.exceptions import EmptyResultSet, FullResultSet
from django.db.models.expressions import Case, When
from django.db.models.lookups import Exact
from django.utils import tree
from django.utils.functional import cached_property
from django.db.models.sql.where import WhereNode
from django.contrib.auth.models import User

def test_replace_expressions():
    # Create a mock WhereNode with some child nodes
    child_node_1 = WhereNode()
    child_node_2 = WhereNode()
    original_node = WhereNode()
    original_node.children = [child_node_1, child_node_2]
    original_node.connector = operator.and_
    original_node.negated = False

    # Create replacements for the nodes
    replacements = {
        original_node: WhereNode(),
        child_node_1: WhereNode(),
    }

    # Call the replace_expressions method
    result_node = original_node.replace_expressions(replacements)

    # Assert the returned node is a clone and check its properties
    assert result_node.connector == original_node.connector
    assert result_node.negated == original_node.negated
    assert len(result_node.children) == 2
    
    # Check if the first child node has been replaced
    assert isinstance(result_node.children[0], WhereNode)
    assert result_node.children[0] is not child_node_1  # Check it is a different instance
    assert result_node.children[1] is child_node_2  # Check the second child remains the same

    # Check if the correct expression was substituted
    assert result_node.children[0] == replacements[child_node_1]
    
    # Assert the original children are unmodified
    assert original_node.children[0] is child_node_1
    assert original_node.children[1] is child_node_2