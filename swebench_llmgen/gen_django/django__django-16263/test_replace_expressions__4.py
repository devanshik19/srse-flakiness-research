import pytest
from django.db.models.sql.where import WhereNode
from django.contrib.auth.models import User

@pytest.fixture
def setup_where_node():
    # Create a mock WhereNode instance
    node = WhereNode()
    return node

def test_replace_expressions_no_replacements(setup_where_node):
    node = setup_where_node
    node.children = []  # No children to replicate

    replacements = {}
    result = node.replace_expressions(replacements)

    assert result is not node  # Ensure it's a clone
    assert result.children == []  # No children should be cloned

def test_replace_expressions_with_replacement(setup_where_node):
    node = setup_where_node
    child_node = WhereNode()
    node.children = [child_node]

    replacements = {node: 'replacement_node'}
    result = node.replace_expressions(replacements)

    assert result == 'replacement_node'  # Should return the replacement directly
    assert result != node  # Ensure it's not the original node

def test_replace_expressions_with_complex_children(setup_where_node):
    node = setup_where_node
    child_node1 = WhereNode()
    child_node2 = WhereNode()
    node.children = [child_node1, child_node2]

    replacements = {child_node1: 'replacement_child'}

    result = node.replace_expressions(replacements)

    assert len(result.children) == 2  # Both children should be present in the clone
    assert result.children[0] == 'replacement_child'  # First child replaced
    assert result.children[1] == child_node2  # Second child remains the same