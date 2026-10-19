import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query
from django.core.exceptions import FieldError, TypeError

@pytest.fixture
def user_query():
    # Create a Query object for User
    return Query(User, alias_cols=[])

def test_build_filter_invalid_dict(user_query):
    with pytest.raises(FieldError, match="Cannot parse keyword query as dict"):
        user_query.build_filter({'username': 'test'})

def test_build_filter_invalid_q(user_query):
    with pytest.raises(TypeError, match="Cannot filter against a non-conditional expression."):
        user_query.build_filter(Q(username='test').resolve_expression(user_query))

def test_build_filter_no_arg(user_query):
    with pytest.raises(FieldError, match="Cannot parse keyword query None"):
        user_query.build_filter((None, 'test'))

def test_build_filter_check_filterable(user_query):
    user_query.alias_refcount['user'] = 1  # Simulate having an alias
    with pytest.raises(FieldError):
        user_query.build_filter(('username', 'test'), check_filterable=True)

def test_build_filter_success(user_query):
    user_query.alias_refcount['user'] = 1  # Simulate having an alias
    user_query.get_meta = lambda: None  # Mock get_meta to return None for testing
    user_query.get_initial_alias = lambda: 'user_alias'  # Mock alias returning
    user_query.check_filterable = lambda x: None  # Allow filter checking
    user_query.resolve_lookup_value = lambda value, *args: value  # Mock resolving lookup value
    user_query.build_lookup = lambda lookups, ref, value: (lookups, ref, value)  # Mock building lookup
    
    clause, used_joins = user_query.build_filter(('username', 'test'))

    assert clause is not None
    assert used_joins == set()