import collections
import re
from functools import partial
from itertools import chain
from django.core.exceptions import EmptyResultSet, FieldError
from django.db import DatabaseError, NotSupportedError
from django.db.models.constants import LOOKUP_SEP
from django.db.models.expressions import F, OrderBy, RawSQL, Ref, Value
from django.db.models.functions import Cast, Random
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
from django.db import connection
import pytest

@pytest.mark.parametrize("result_type, chunked_fetch, expected", [
    (MULTI, False, []),  # No results expected scenario
    (SINGLE, False, None),  # No results expected for SINGLE
    (CURSOR, False, 'cursor'),  # To test CURSOR return
])
def test_execute_sql_empty_results(mocked_cursor, result_type, chunked_fetch, expected):
    # Setup
    compiler = SQLCompiler(query=Query(User), connection=connection)
    
    # Mock the as_sql function
    compiler.as_sql = lambda: ("", [])
    
    # Testing for various result types
    if expected == 'cursor':
        cursor_result = compiler.execute_sql(result_type=result_type, chunked_fetch=chunked_fetch)
        assert isinstance(cursor_result, collections.abc.Iterator)
    else:
        assert compiler.execute_sql(result_type=result_type, chunked_fetch=chunked_fetch) == expected

@pytest.mark.parametrize("result_type, chunked_fetch, expected", [
    (SINGLE, False, 'result'),
    (MULTI, False, ['result1', 'result2']),
])
def test_execute_sql_valid_results(mocked_cursor, result_type, chunked_fetch, expected):
    # Setup
    compiler = SQLCompiler(query=Query(User), connection=connection)

    # Mocking the as_sql method to return a valid query
    compiler.as_sql = lambda: ("SELECT * FROM auth_user", [])

    mocked_cursor.fetchall.return_value = expected if result_type == MULTI else [expected]
    mocked_cursor.fetchone.return_value = expected if result_type == SINGLE else None

    # Testing the execute_sql method
    results = compiler.execute_sql(result_type=result_type, chunked_fetch=chunked_fetch)
    assert results == (expected if result_type == MULTI else expected[0] if expected else None)

@pytest.mark.parametrize("result_type", [CURSOR, NO_RESULTS])
def test_execute_sql_cursor_or_no_results(mocked_cursor, result_type):
    # Setup
    compiler = SQLCompiler(query=Query(User), connection=connection)

    # Mocking the as_sql method to return a valid SQL
    compiler.as_sql = lambda: ("SELECT * FROM auth_user", [])

    # Mock cursor behavior
    if result_type == CURSOR:
        cursor = compiler.execute_sql(result_type=result_type)
        assert cursor == mocked_cursor
    else:
        assert compiler.execute_sql(result_type=result_type) is None