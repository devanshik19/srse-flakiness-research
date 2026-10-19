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
    BaseExpression, Col, Exists, F, OuterRef, Ref, ResolvedOuterRef,
)
from django.db.models.fields import Field
from django.db.models.fields.related_lookups import MultiColSource
from django.db.models.lookups import Lookup
from django.db.models.query_utils import (
    Q, check_rel_lookup_compatibility, refs_expression,
)
from django.db.models.sql.constants import INNER, LOUTER, ORDER_DIR, SINGLE
from django.db.models.sql.datastructures import (
    BaseTable, Empty, Join, MultiJoin,
)
from django.db.models.sql.where import (
    AND, OR, ExtraWhere, NothingNode, WhereNode,
)
from django.utils.functional import cached_property
from django.utils.tree import Node
from django.db.models import QuerySet
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_change_aliases():
    # Setup initial query with select, group_by and alias_map
    user_query = User.objects.all()
    query = Query(User, alias_cols=False)
    query.select = (Col('id'),)
    query.group_by = (Col('username'),)
    query.alias_map = {
        'user': query.base_table_class('auth_user', 'user'),
    }
    query.alias_refcount = {'user': 1}
    query.external_aliases = {'user': False}

    change_map = {
        'user': 'new_user',
    }

    # Call change_aliases method
    query.change_aliases(change_map)

    # Assertions to ensure aliases are changed correctly
    assert 'new_user' in query.alias_map
    assert 'user' not in query.alias_map
    assert query.alias_refcount['new_user'] == 1
    assert 'user' not in query.alias_refcount
    assert all(alias == 'new_user' for alias in query.table_map[query.base_table_class('auth_user', 'new_user')])
    assert query.external_aliases['new_user'] is True

    # Additional checks for the select and group by columns
    assert query.select[0].alias == 'new_user.id'  # assuming relabeling happens for Col
    assert query.group_by[0].alias == 'new_user.username'  # assuming same for group_by