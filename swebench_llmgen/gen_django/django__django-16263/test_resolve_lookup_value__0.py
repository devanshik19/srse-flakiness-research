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
    Value,
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
from django.utils.regex_helper import _lazy_re_compile
from django.utils.tree import Node
from django.db.models import QuerySet
from django.contrib.auth.models import User


class TestQuery:
    
    def setup_method(self):
        self.query = Query(User.objects.all())
        
    def test_resolve_lookup_value_expression(self):
        user_instance = User.objects.create(username='testuser')
        expression = Value(user_instance.username)
        resolved = self.query.resolve_lookup_value(expression, True, True)
        assert resolved == user_instance.username

    def test_resolve_lookup_value_list(self):
        user_instance1 = User.objects.create(username='user1')
        user_instance2 = User.objects.create(username='user2')
        resolved = self.query.resolve_lookup_value([user_instance1.username, user_instance2.username], True, True)
        assert resolved == [user_instance1.username, user_instance2.username]

    def test_resolve_lookup_value_tuple(self):
        user_instance1 = User.objects.create(username='user1')
        user_instance2 = User.objects.create(username='user2')
        resolved = self.query.resolve_lookup_value((user_instance1.username, user_instance2.username), True, True)
        assert resolved == (user_instance1.username, user_instance2.username)

    def test_resolve_lookup_value_namedtuple(self):
        UserTuple = namedtuple('UserTuple', ['username'])
        user_instance = User.objects.create(username='nameduser')
        resolved = self.query.resolve_lookup_value(UserTuple(user_instance.username), True, True)
        assert resolved.username == user_instance.username

    def test_resolve_lookup_value_when_no_expression(self):
        resolved = self.query.resolve_lookup_value('simple_value', True, True)
        assert resolved == 'simple_value'