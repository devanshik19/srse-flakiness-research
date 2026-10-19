import operator
from functools import reduce
from django.core.exceptions import EmptyResultSet, FullResultSet
from django.db.models.expressions import Case, When
from django.db.models.lookups import Exact
from django.utils import tree
from django.utils.functional import cached_property
from django.contrib.auth.models import User
from django.db.models import Q

class WhereNode:
    def __init__(self, children=None, connector=None, negated=False):
        self.children = children or []
        self.connector = connector
        self.negated = negated

    def replace_expressions(self, replacements):
        if replacement := replacements.get(self):
            return replacement
        clone = self.create(connector=self.connector, negated=self.negated)
        for child in self.children:
            clone.children.append(child.replace_expressions(replacements))
        return clone

    def create(self, connector, negated):
        return WhereNode(connector=connector, negated=negated)

def test_replace_expressions_replaces_node():
    original_node = WhereNode(children=[], connector=operator.and_, negated=False)
    replacement_node = WhereNode(children=[], connector=operator.or_, negated=True)
    replacements = {original_node: replacement_node}

    result = original_node.replace_expressions(replacements)

    assert result is replacement_node

def test_replace_expressions_clones_node():
    original_node = WhereNode(children=[], connector=operator.and_, negated=False)
    replacements = {}

    result = original_node.replace_expressions(replacements)

    assert result is not original_node
    assert result.connector == original_node.connector
    assert result.negated == original_node.negated
    assert result.children == []

def test_replace_expressions_replaces_children():
    child_node = WhereNode(children=[], connector=operator.and_, negated=False)
    original_node = WhereNode(children=[child_node], connector=operator.and_, negated=False)
    replacement_child_node = WhereNode(children=[], connector=operator.or_, negated=True)
    replacements = {child_node: replacement_child_node}

    result = original_node.replace_expressions(replacements)

    assert len(result.children) == 1
    assert result.children[0] is replacement_child_node

def test_replace_expressions_no_replacements():
    original_node = WhereNode(children=[], connector=operator.and_, negated=False)
    replacements = {}

    result = original_node.replace_expressions(replacements)

    assert result is not original_node
    assert len(result.children) == 0
    assert result.connector == original_node.connector
    assert result.negated == original_node.negated