import pytest
from django.db.models.sql.where import WhereNode
from django.contrib.auth.models import User

@pytest.fixture
def setup_where_node():
    # Create instances of WhereNode as children to form the test subject
    # This will require a simple subclass or just a dummy where node.
    node1 = WhereNode()
    node2 = WhereNode()
    node1.children = []
    node2.children = []
    parent_node = WhereNode()
    parent_node.children = [node1, node2]
    parent_node.connector = 'AND'
    parent_node.negated = False
    return parent_node, {node1: 'replacement1', node2: 'replacement2'}

def test_replace_expressions(setup_where_node):
    parent_node, replacements = setup_where_node
    
    # Call the method with actual replacements
    result_node = parent_node.replace_expressions(replacements)
    
    # Check if the returned node is not the same reference as the original parent_node
    assert result_node is not parent_node
    
    # Check if the replacements were made correctly
    assert len(result_node.children) == 2
    assert result_node.children[0] == 'replacement1'
    assert result_node.children[1] == 'replacement2'
    
    # Check that the connector and negation are preserved
    assert result_node.connector == parent_node.connector
    assert result_node.negated == parent_node.negated
    
    # Test with no replacements to ensure original children are retained
    result_node_no_replacements = parent_node.replace_expressions({})
    assert result_node_no_replacements is not parent_node
    assert result_node_no_replacements.children == parent_node.children