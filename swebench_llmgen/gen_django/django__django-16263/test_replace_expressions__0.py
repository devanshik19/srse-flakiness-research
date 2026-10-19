import operator
from functools import reduce
from django.core.exceptions import EmptyResultSet, FullResultSet
from django.db.models.expressions import Case, When
from django.db.models.lookups import Exact
from django.utils import tree
from django.utils.functional import cached_property
from django.contrib.auth.models import User
from django.db.models.sql.where import WhereNode

def test_replace_expressions():
    # Create instances of WhereNode
    node1 = WhereNode()
    node2 = WhereNode()
    node3 = WhereNode()

    # Setting up a mock connector and children
    node1.connector = operator.and_
    node1.negated = False
    node1.children = [node2, node3]

    # Define replacements
    replacements = {
        node1: WhereNode(),  # Replace node1 with a new WhereNode instance
    }

    # Perform the replacement
    result = node1.replace_expressions(replacements)

    # Check if the replacement was successful
    assert result is not node1  # Ensure the result is not the same object
    assert result.children == [node2, node3]  # Children should remain the same
    assert result.connector == node1.connector  # Connector should be the same
    assert result.negated == node1.negated  # Negated should be the same

    # Test with no applicable replacement
    replacements = {node2: WhereNode()}  # Only node2 is present in replacements
    result_without_replacement = node1.replace_expressions(replacements)

    # Ensure the original structure is intact where no replacement occurred
    assert result_without_replacement is not node1
    assert result_without_replacement.children == [node2, node3]  # Still unchanged
    assert result_without_replacement.connector == node1.connector
    assert result_without_replacement.negated == node1.negated