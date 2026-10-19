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
from django.db import connection
from django.contrib.auth.models import User
import pytest

class SQLCompiler:
    # Assuming other methods/fields exist in this class as stated
    def __init__(self, query, connection, using):
        self.query = query
        self.connection = connection
        self.using = using
        self.col_count = 3  # Assuming we have 3 columns to fetch
        self.has_extra_select = False

    def as_sql(self):
        # Simulate a SQL statement and its parameters
        return "SELECT id, username, email FROM auth_user", []

    def execute_sql(self, result_type=MULTI, chunked_fetch=False, chunk_size=GET_ITERATOR_CHUNK_SIZE):
        result_type = result_type or NO_RESULTS
        try:
            sql, params = self.as_sql()
            if not sql:
                raise EmptyResultSet
        except EmptyResultSet:
            if result_type == MULTI:
                return iter([])
            else:
                return
        cursor = self.connection.cursor() if not chunked_fetch else self.connection.chunked_cursor()
        try:
            cursor.execute(sql, params)
        except Exception:
            cursor.close()
            raise

        if result_type == CURSOR:
            return cursor
        if result_type == SINGLE:
            try:
                val = cursor.fetchone()
                if val:
                    return val[0:self.col_count]
                return val
            finally:
                cursor.close()
        if result_type == NO_RESULTS:
            cursor.close()
            return

        result = cursor.fetchall()  # Using fetchall for MULTI
        cursor.close()
        return result


def test_execute_sql():
    user = User.objects.create_user(username='testuser', password='password', email='test@example.com')
    
    compiler = SQLCompiler(query=None, connection=connection, using='default')

    # Test MULTI result type
    results = compiler.execute_sql(result_type=MULTI)
    assert isinstance(results, list)
    assert len(results) == 1
    assert results[0][1] == 'testuser'  # username

    # Test SINGLE result type
    single_result = compiler.execute_sql(result_type=SINGLE)
    assert isinstance(single_result, tuple)
    assert single_result[1] == 'testuser'  # username

    # Test CURSOR result type
    cursor = compiler.execute_sql(result_type=CURSOR)
    row = cursor.fetchone()
    assert row[1] == 'testuser'  # username
    cursor.close()

    # Test NO_RESULTS
    empty_compiler = SQLCompiler(query=None, connection=connection, using='default')
    assert empty_compiler.execute_sql(result_type=NO_RESULTS) is None