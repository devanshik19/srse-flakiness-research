import pytest
from django.contrib.auth.models import User
from django.db.models.sql.compiler import SQLCompiler
from django.db.models import F, OrderBy
from django.db.models.sql.query import Query
from django.db.models.constants import LOOKUP_SEP
from django.core.exceptions import FieldError

@pytest.fixture
def compiler():
    query = Query(User)
    return SQLCompiler(query=query, connection=None, using=None)

def test_find_ordering_name_simple(compiler):
    opts = User._meta
    result = compiler.find_ordering_name('username', opts)
    assert len(result) == 1
    assert isinstance(result[0][0], OrderBy)
    assert result[0][0].expression == F('username')
    assert result[0][0].descending is False

def test_find_ordering_name_descending(compiler):
    opts = User._meta
    result = compiler.find_ordering_name('username__desc', opts)
    assert len(result) == 1
    assert isinstance(result[0][0], OrderBy)
    assert result[0][0].expression == F('username')
    assert result[0][0].descending is True

def test_find_ordering_name_with_related_field(compiler):
    opts = User._meta
    result = compiler.find_ordering_name('groups__name', opts)
    assert len(result) == 1
    assert isinstance(result[0][0], OrderBy)
    assert 'groups' in str(result[0][0].expression)

def test_find_ordering_name_infinite_loop(compiler):
    opts = User._meta
    # Simulating an infinite relation loop by setting up a circular reference
    with pytest.raises(FieldError, match='Infinite loop caused by ordering.'):
        compiler.find_ordering_name('groups__users__groups__name', opts)

def test_find_ordering_name_with_default_order(compiler):
    opts = User._meta
    result = compiler.find_ordering_name('username', opts, default_order='DESC')
    assert len(result) == 1
    assert result[0][0].descending is True