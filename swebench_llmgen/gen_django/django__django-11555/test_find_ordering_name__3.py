import pytest
from django.contrib.auth.models import User
from django.db.models.sql.compiler import SQLCompiler
from django.db.models import Q
from django.core.exceptions import FieldError

@pytest.fixture
def sql_compiler():
    # Create a dummy query for the SQLCompiler
    from django.db.models.sql.query import Query
    from django.db import connections

    # Initialize a query with the User model
    query = Query(User._meta)
    connection = connections['default']
    return SQLCompiler(query, connection, using='default')

def test_find_ordering_name_basic(sql_compiler):
    result = sql_compiler.find_ordering_name('username', User._meta)
    assert len(result) == 1
    assert result[0][0].expression.name == 'username'
    assert result[0][1] is False

def test_find_ordering_name_descending(sql_compiler):
    result = sql_compiler.find_ordering_name('username__desc', User._meta)
    assert len(result) == 1
    assert result[0][0].expression.name == 'username'
    assert result[0][0].descending is True

def test_find_ordering_name_with_relation(sql_compiler):
    # Assume 'groups' is a related field in User model
    result = sql_compiler.find_ordering_name('groups__name', User._meta)
    assert len(result) > 0  # The actual number needs consideration based on models

def test_find_ordering_name_infinite_loop(sql_compiler):
    sql_compiler.query.alias_map = {'app_user': sql_compiler.query.alias_map}  # Simulate a recursive join
    with pytest.raises(FieldError, match='Infinite loop caused by ordering.'):
        sql_compiler.find_ordering_name('groups__name', User._meta)

def test_find_ordering_name_default_order(sql_compiler):
    result = sql_compiler.find_ordering_name('is_active', User._meta)
    assert len(result) == 1
    assert result[0][0].expression.name == 'is_active'
    assert result[0][1] is False