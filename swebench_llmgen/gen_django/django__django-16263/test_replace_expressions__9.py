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
    # Setup: Create a mock WhereNode and some replacements
    original_node = WhereNode()
    original_node.connector = 'AND'
    original_node.negated = False
    original_node.children = [WhereNode(), WhereNode()]

    # Create a replacement node
    replacement_node = WhereNode()
    replacement_node.connector = 'OR'
    replacement_node.negated = True
    replacement_node.children = []

    # Create a replacements dictionary to use for testing
    replacements = {original_node: replacement_node}

    # Invoke the replace_expressions method
    new_node = original_node.replace_expressions(replacements)

    # Assertions
    assert new_node is not original_node  # ensure a new instance is returned
    assert new_node.connector == 'AND'  # should retain original connector
    assert new_node.negated is False  # should retain original negation
    assert len(new_node.children) == 2  # original children count should be retained

    # Validate that the child WhereNode's replace_expressions are called
    for child in new_node.children:
        # Ensure that children are untouched
        assert child is not node.children[0] and child is not node.children[1]
        assert isinstance(child, WhereNode)  # confirm that children are still WhereNodes

    # Test the replacement when original node is not in replacements
    unreplaced_node = WhereNode()
    unreplaced_node.connector = 'AND'
    unreplaced_node.negated = False
    unreplaced_node.children = []

    new_unreplaced_node = unreplaced_node.replace_expressions(replacements)
    assert new_unreplaced_node is not unreplaced_node  # should be a new instance
    assert new_unreplaced_node.connector == 'AND'  # should keep the same connector
    assert new_unreplaced_node.children == []  # should have no children