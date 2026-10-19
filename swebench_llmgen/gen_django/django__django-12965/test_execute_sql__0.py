import collections
import re
from functools import partial
from itertools import chain
from django.core.exceptions import EmptyResultSet, FieldError
from django.db import DatabaseError, NotSupportedError
from django.db.models.constants import LOOKUP_SEP
from django.db.models.expressions import OrderBy, Random, RawSQL, Ref, Value
from django.db.models.functions import Cast
from django.db.models.query_utils import Q, select_related_descend
from django.db.models.sql.constants import (
    CURSOR, GET_ITERATOR_CHUNK_SIZE, MULTI, NO_RESULTS, ORDER_DIR, SINGLE,
)
from django.db.models.sql.query import Query, get_order_dir
from django.db.transaction import TransactionManagementError
from django.utils.functional import cached_property
from django.utils.hashable import make_hashable
from django.utils.regex_helper import _lazy_re_compile
from django.contrib.auth.models import User
from django.db.models.sql.compiler import SQLCompiler

def test_execute_sql_multiple_results(db):
    user1 = User.objects.create(username='user1', password='password')
    user2 = User.objects.create(username='user2', password='password')
    query = User.objects.all()
    
    compiler = SQLCompiler(query.query, query.model._meta.db_table) 
    result = compiler.execute_sql(result_type=MULTI)

    assert len(list(result)) == 2

def test_execute_sql_single_result(db):
    user = User.objects.create(username='single_user', password='password')
    query = User.objects.filter(username='single_user')

    compiler = SQLCompiler(query.query, query.model._meta.db_table)
    result = compiler.execute_sql(result_type=SINGLE)

    assert result.username == 'single_user'

def test_execute_sql_no_results(db):
    query = User.objects.filter(pk=-1)  # Assuming this ID does not exist

    compiler = SQLCompiler(query.query, query.model._meta.db_table)
    result = compiler.execute_sql(result_type=MULTI)

    assert list(result) == []

def test_execute_sql_cursor_result(db):
    user = User.objects.create(username='cursor_user', password='password')
    query = User.objects.all()

    compiler = SQLCompiler(query.query, query.model._meta.db_table)
    cursor_result = compiler.execute_sql(result_type=CURSOR)

    assert cursor_result.fetchone() is not None

def test_execute_sql_empty_query(db):
    class EmptyQuery:
        def as_sql(self):
            return '', []

    query = EmptyQuery()
    compiler = SQLCompiler(query, 'fake_table')

    with pytest.raises(EmptyResultSet):
        compiler.execute_sql(result_type=MULTI)