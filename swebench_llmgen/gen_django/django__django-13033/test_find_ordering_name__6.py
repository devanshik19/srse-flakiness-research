import pytest
from django.contrib.auth.models import User
from django.db.models import F
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query
from django.db.models.sql.constants import ORDER_DIR

@pytest.fixture
def sql_compiler():
    query = Query(User)  # Using the User model for the query
    return SQLCompiler(query=query, connection=query.get_connection(), using=query.get_connection().alias)

def test_find_ordering_name_ascending(sql_compiler):
    opts = User._meta
    ordering = sql_compiler.find_ordering_name('username', opts)
    assert len(ordering) == 1
    assert ordering[0][0].expression == F('username')
    assert ordering[0][0].descending is False

def test_find_ordering_name_descending(sql_compiler):
    opts = User._meta
    ordering = sql_compiler.find_ordering_name('username__DESC', opts)
    assert len(ordering) == 1
    assert ordering[0][0].expression == F('username')
    assert ordering[0][0].descending is True

def test_find_ordering_name_infinite_loop(sql_compiler):
    opts = User._meta
    sql_compiler.query.alias_map = {'a': sql_compiler.query.alias_map.get('a')}  # Simulating a loop
    with pytest.raises(FieldError, match='Infinite loop caused by ordering'):
        sql_compiler.find_ordering_name('related_model__field', opts)

def test_find_ordering_name_with_default_ordering(sql_compiler):
    opts = User._meta
    opts.ordering = ['date_joined']
    ordering = sql_compiler.find_ordering_name('date_joined', opts)
    assert len(ordering) == 1
    assert ordering[0][0].expression == F('date_joined')
    assert ordering[0][0].descending is False

def test_find_ordering_name_no_relation(sql_compiler):
    opts = User._meta
    ordering = sql_compiler.find_ordering_name('email', opts)
    assert len(ordering) == 1
    assert ordering[0][0].expression == F('email')
    assert ordering[0][0].descending is False