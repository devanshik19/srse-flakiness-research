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
from django.db.models import QuerySet
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
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_set_values():
    # Setup
    user_query = Query(User)
    
    # Test with specific field names
    user_query.set_values(['username', 'email'])
    assert user_query.values_select == ('username', 'email')
    
    # Ensure that select_related is set to False
    assert not user_query.select_related
    
    # Check that extra and annotation names are empty
    assert user_query.extra_select_mask == ()
    assert user_query.annotation_select_mask == ()
    
    # Test with fields including extra fields
    user_query.extra_select = {'extra_field': 'COUNT(*)'}
    user_query.annotation_select = {'annotated_field': 'MAX(date_joined)'}
    
    user_query.set_values(['username', 'extra_field', 'annotated_field'])
    assert user_query.values_select == ('username', 'extra_field', 'annotated_field')
    assert user_query.extra_select_mask == ('extra_field',)
    assert user_query.annotation_select_mask == ('annotated_field',)
    
    # Test with empty fields
    user_query.set_values([])
    assert user_query.values_select == tuple(f.attname for f in user_query.model._meta.concrete_fields)
    
    # Test group_by True
    user_query.group_by = True
    user_query.set_values(['username'])
    assert user_query.group_by is not True
    assert user_query.values_select == ('username',)
    
    # Check that clearing select fields worked
    user_query.clear_select_fields()
    assert not user_query.has_select_fields()