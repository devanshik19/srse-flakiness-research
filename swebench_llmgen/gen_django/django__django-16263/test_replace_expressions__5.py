import operator
from functools import reduce
from django.core.exceptions import EmptyResultSet, FullResultSet
from django.db.models.expressions import Case, When
from django.db.models.lookups import Exact
from django.utils import tree
from django.utils.functional import cached_property
from django.db.models.sql.where import WhereNode
from django.contrib.auth.models import User
import pytest


@pytest.fixture
def where_node():
    return WhereNode()


def test_replace_expressions_no_replacement(where_node):
    replacements = {}
    assert where_node.replace_expressions(replacements) == where_node.clone()


def test_replace_expressions_with_replacement(where_node):
    replacement_node = WhereNode()
    replacements = {where_node: replacement_node}
    
    result = where_node.replace_expressions(replacements)
    
    assert result == replacement_node


def test_replace_expressions_with_children(where_node):
    child_node = WhereNode()
    where_node.children = [child_node]
    
    replacements = {child_node: WhereNode()}
    
    result = where_node.replace_expressions(replacements)
    
    assert len(result.children) == 1
    assert isinstance(result.children[0], WhereNode)