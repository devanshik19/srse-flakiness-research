import pytest
from django.contrib.auth.models import User
from django.db.models.sql.where import WhereNode

@pytest.fixture
def setup_where_node():
    user = User.objects.create_user(username='testuser', password='testpass')
    parent_node = WhereNode()
    child_node_1 = WhereNode()
    child_node_2 = WhereNode()
    parent_node.children = [child_node_1, child_node_2]
    parent_node.connector = 'AND'
    parent_node.negated = False
    return parent_node, {parent_node: WhereNode()}

def test_replace_expressions_no_replacement(setup_where_node):
    parent_node, replacements = setup_where_node
    result = parent_node.replace_expressions({})
    assert result is not parent_node
    assert result.children == parent_node.children
    assert result.connector == parent_node.connector
    assert result.negated == parent_node.negated

def test_replace_expressions_with_replacement(setup_where_node):
    parent_node, replacements = setup_where_node
    replacement_node = replacements[parent_node]
    assert replacement_node is not None
    result = parent_node.replace_expressions(replacements)
    assert result is replacement_node

def test_replace_expressions_with_nested_children(setup_where_node):
    parent_node, replacements = setup_where_node
    nested_replacement = WhereNode()
    replacements[parent_node.children[0]] = nested_replacement
    result = parent_node.replace_expressions(replacements)
    assert result.children[0] is nested_replacement
    assert result.children[1] is parent_node.children[1]