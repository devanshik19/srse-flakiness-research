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

class QueryTests:

    def test_output_field_single_select(self):
        user = User.objects.create(username='testuser')
        query = Query()
        query.select = [Col('username', User)]  # Assuming 'username' exists
        query.annotation_select = {}
        result = query.output_field()
        assert result is not None
        assert result == query.select[0].field

    def test_output_field_single_annotation_select(self):
        user = User.objects.create(username='testuser')
        query = Query()
        query.select = []
        query.annotation_select = {'username_annotation': Col('username', User)}  # Assuming 'username' exists
        result = query.output_field()
        assert result is not None
        assert result == query.annotation_select['username_annotation'].output_field

    def test_output_field_no_selects(self):
        query = Query()
        query.select = []
        query.annotation_select = {}
        result = query.output_field()
        assert result is None

    def test_output_field_multiple_selects(self):
        query = Query()
        query.select = [Col('first_name', User), Col('last_name', User)]
        query.annotation_select = {}
        result = query.output_field()
        assert result is None