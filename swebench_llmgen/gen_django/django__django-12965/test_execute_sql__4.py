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
from django.db.models.sql.query import Query
from django.db.models.sql.compiler import SQLCompiler
from django.contrib.auth.models import User

def test_execute_sql_single(cursor):
    user = User.objects.create(username='test_user')
    compiler = SQLCompiler(query=User.objects.filter(username='test_user').query, connection=cursor)
    
    result = compiler.execute_sql(result_type=SINGLE)
    
    assert result is not None
    assert result[0] == user.username

def test_execute_sql_multi(cursor):
    User.objects.create(username='user1')
    User.objects.create(username='user2')
    compiler = SQLCompiler(query=User.objects.all().query, connection=cursor)
    
    result = list(compiler.execute_sql(result_type=MULTI))
    
    assert len(result) == 2
    assert result[0][0] in ['user1', 'user2']
    assert result[1][0] in ['user1', 'user2']

def test_execute_sql_no_results(cursor):
    compiler = SQLCompiler(query=User.objects.filter(username='non_existent_user').query, connection=cursor)
    
    result = compiler.execute_sql(result_type=MULTI)
    
    assert result == iter([])

def test_execute_sql_cursor(cursor):
    user = User.objects.create(username='cursor_user')
    compiler = SQLCompiler(query=User.objects.filter(username='cursor_user').query, connection=cursor)
    
    result_cursor = compiler.execute_sql(result_type=CURSOR)
    
    assert result_cursor is not None
    row = result_cursor.fetchone()
    assert row is not None
    assert row[0] == user.username
    
    result_cursor.close()

def test_execute_sql_empty_query(cursor):
    compiler = SQLCompiler(query=User.objects.none().query, connection=cursor)
    
    with pytest.raises(EmptyResultSet):
        compiler.execute_sql(result_type=MULTI)

def test_execute_sql_chunked_fetch(cursor):
    User.objects.create(username='chunk_user1')
    User.objects.create(username='chunk_user2')
    compiler = SQLCompiler(query=User.objects.all().query, connection=cursor)
    
    result = list(compiler.execute_sql(chunked_fetch=True, result_type=MULTI))
    
    assert len(result) == 2
    assert result[0][0] in ['chunk_user1', 'chunk_user2']
    assert result[1][0] in ['chunk_user1', 'chunk_user2']