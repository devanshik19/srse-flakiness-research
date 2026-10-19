import pytest
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.db.models import F, OrderBy
from django.db.models.sql.query import Query
from django.db.models.sql.compiler import SQLCompiler

@pytest.fixture
def compiler():
    # Create a dummy Query and a SQLCompiler instance for testing
    query = Query(User)
    return SQLCompiler(query, None, None)

@pytest.mark.parametrize("name, default_order, expected", [
    ("username", "ASC", [(OrderBy(F('username'), descending=False), False)]),
    ("date_joined", "DESC", [(OrderBy(F('date_joined'), descending=True), False)]),
    ("email__contains", "ASC", [(OrderBy(F('email'), descending=False), False)]),
])
def test_find_ordering_name_basic(compiler, name, default_order, expected):
    user_opts = User._meta
    result = compiler.find_ordering_name(name, user_opts, default_order=default_order)
    assert result == expected

def test_find_ordering_name_infinite_loop(compiler):
    user_opts = User._meta
    compiler.query.alias_map = {0: type('Alias', (), {"join_cols": None})}
    compiler.query.fields = ['username', 'email']
    
    # Dummy case to cause infinite detection
    compiler.query.alias_map[1] = type('Alias', (), {"join_cols": None})
    compiler.query.alias_map[2] = type('Alias', (), {"join_cols": None})
    
    with pytest.raises(FieldError, match='Infinite loop caused by ordering.'):
        compiler.find_ordering_name('username', user_opts, already_seen={((None, None),)})

def test_find_ordering_name_relation(compiler):
    user_opts = User._meta
    result = compiler.find_ordering_name('username', user_opts)
    
    # Check for relation ordering
    assert isinstance(result[0][0], OrderBy)
    assert result[0][0].expression.name == 'username' 

def test_find_ordering_name_default_no_results(compiler):
    user_opts = User._meta
    result = compiler.find_ordering_name('nonexistent_field', user_opts)
    
    assert result == []