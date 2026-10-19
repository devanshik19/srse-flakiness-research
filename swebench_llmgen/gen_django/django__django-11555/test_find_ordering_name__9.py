import pytest
from django.contrib.auth.models import User
from django.db.models.sql.compiler import SQLCompiler
from django.db.models import F

@pytest.fixture
def sql_compiler():
    user_queryset = User.objects.all()
    return SQLCompiler(query=user_queryset.query, connection=user_queryset.db)

def test_find_ordering_name_ascending(sql_compiler):
    opts = User._meta
    alias = None
    name = 'username'  # simple field
    result = sql_compiler.find_ordering_name(name, opts, alias, default_order='ASC')
    assert len(result) == 1
    assert result[0][0].expression.name == 'username'
    assert result[0][0].descending is False

def test_find_ordering_name_descending(sql_compiler):
    opts = User._meta
    alias = None
    name = 'username__username'  # ambiguous field
    result = sql_compiler.find_ordering_name(name, opts, alias, default_order='DESC')
    assert len(result) == 1
    assert result[0][0].expression.name == 'username'
    assert result[0][0].descending is True

def test_find_ordering_name_with_relation(sql_compiler):
    opts = User._meta
    alias = None
    # Assumption: a related field that triggers default ordering
    name = 'groups__name'  # using a related model
    result = sql_compiler.find_ordering_name(name, opts, alias, default_order='ASC')
    assert isinstance(result, list)

def test_find_ordering_name_infinite_loop(sql_compiler):
    opts = User._meta
    alias = None
    with pytest.raises(FieldError, match='Infinite loop caused by ordering.'):
        sql_compiler.find_ordering_name('groups__user__groups__name', opts, alias, default_order='ASC')

def test_find_ordering_name_no_results(sql_compiler):
    opts = User._meta
    alias = None
    result = sql_compiler.find_ordering_name('non_existent_field', opts, alias)
    assert result == []