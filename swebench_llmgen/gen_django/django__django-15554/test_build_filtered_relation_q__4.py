import copy
import difflib
import functools
import sys
from collections import Counter, namedtuple
from collections.abc import Iterator, Mapping
from itertools import chain, count, product
from string import ascii_uppercase
from django.core.exceptions import FieldDoesNotExist, FieldError
from django.db import DEFAULT_DB_ALIAS, NotSupportedError, connections
from django.db.models.aggregates import Count
from django.db.models.constants import LOOKUP_SEP
from django.db.models.expressions import (
    BaseExpression,
    Col,
    Exists,
    F,
    OuterRef,
    Ref,
    ResolvedOuterRef,
)
from django.db.models.fields import Field
from django.db.models.fields.related_lookups import MultiColSource
from django.db.models.lookups import Lookup
from django.db.models.query_utils import (
    Q,
    check_rel_lookup_compatibility,
    refs_expression,
)
from django.db.models.sql.constants import INNER, LOUTER, ORDER_DIR, SINGLE
from django.db.models.sql.datastructures import BaseTable, Empty, Join, MultiJoin
from django.db.models.sql.where import AND, OR, ExtraWhere, NothingNode, WhereNode
from django.utils.functional import cached_property
from django.utils.tree import Node
from django.db.models import QuerySet
from django.contrib.auth.models import User
from django.db import models

class QueryTest:
    
    @pytest.fixture
    def setup_users(self):
        User.objects.create_user(username='user1', password='testpass')
        User.objects.create_user(username='user2', password='testpass')
        User.objects.create_user(username='user3', password='testpass')

    def test_build_filtered_relation_q(self, setup_users):
        query = Query(User)

        # Test with a simple Q object (no negation)
        q_object = Q(username='user1')
        result = query.build_filtered_relation_q(q_object, reuse=False)
        assert isinstance(result, WhereNode)
        assert result.connector == AND
        assert len(result.children) == 1
        
        # Test with negation
        q_object = Q(username='user1', negated=True)
        result = query.build_filtered_relation_q(q_object, reuse=False)
        assert isinstance(result, WhereNode)
        assert result.connector == AND
        assert result.negated is True
        assert len(result.children) == 1
        
        # Test with multiple children
        q_object = Q(username='user1') | Q(username='user2')
        result = query.build_filtered_relation_q(q_object, reuse=False)
        assert isinstance(result, WhereNode)
        assert len(result.children) == 2
        
        # Test with complex Q object including negation
        child_q = Q(username='user1') & Q(is_active=True)
        q_object = Q(username='user2', negated=True) | child_q
        result = query.build_filtered_relation_q(q_object, reuse=False)
        assert isinstance(result, WhereNode)
        assert len(result.children) == 2
        assert result.children[0].negated is True  # The first should be negated