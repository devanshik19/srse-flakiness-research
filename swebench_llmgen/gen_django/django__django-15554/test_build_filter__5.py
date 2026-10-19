import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query
from django.core.exceptions import FieldError, TypeError

@pytest.fixture
def user_query():
    return Query(model=User)  # Assume an existing Query object for User

def test_build_filter_with_dict_raises_field_error(user_query):
    with pytest.raises(FieldError, match="Cannot parse keyword query as dict"):
        user_query.build_filter({'username': 'test_user'})

def test_build_filter_with_q_object(user_query):
    q_object = Q(username='test_user')
    where_node, used_joins = user_query.build_filter(q_object)
    assert isinstance(where_node, WhereNode)
    assert len(used_joins) == 0  # No joins for simple Q

def test_build_filter_with_conditional_expression(user_query):
    from django.db.models.expressions import F
    condition_expr = F('username')
    with pytest.raises(TypeError, match="Cannot filter against a non-conditional expression."):
        user_query.build_filter(condition_expr)

def test_build_filter_with_valid_keyword_arg(user_query):
    user_query.check_filterable = lambda x: None  # Stubbing filter check as no-op
    where_node, used_joins = user_query.build_filter(('username', 'test_user'))
    assert isinstance(where_node, WhereNode)

def test_build_filter_with_empty_arg(user_query):
    with pytest.raises(FieldError, match="Cannot parse keyword query"):
        user_query.build_filter(('', 'test_user'))

def test_build_filter_with_unjoined_field(user_query):
    user_query.alias_refcount = {}
    with pytest.raises(FieldError, match="Joined field references are not permitted in this query"):
        user_query.build_filter(('profile__bio', 'test_bio'), allow_joins=False)

def test_build_filter_with_check_filterable_none(user_query):
    user_query.check_filterable = lambda x: None  # No-op to allow filtering
    user_query.alias_refcount = {}
    where_node, used_joins = user_query.build_filter(('username', 'test_user'))
    assert isinstance(where_node, WhereNode)
    assert len(used_joins) == 0

def test_build_filter_with_relational_field(user_query):
    user_query.check_filterable = lambda x: None  # No-op for check_filterable
    user_query.alias_refcount = {}
    user_query.setup_joins = lambda *args, **kwargs: namedtuple('JoinInfo', 'final_field, joins, targets, path')('user', [], [], '')
    user_query.is_nullable = lambda *args: False  # Assume it's not nullable
    where_node, used_joins = user_query.build_filter(('username', 'test_user'))
    assert isinstance(where_node, WhereNode)
    assert len(used_joins) == 0