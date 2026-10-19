import pytest
from django.db.models import Q
from django.core.exceptions import FieldError, TypeError
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def user_query():
    return Query(User)  # Initialize a Query object for User model

def test_build_filter_with_dict_raises_field_error(user_query):
    with pytest.raises(FieldError, match="Cannot parse keyword query as dict"):
        user_query.build_filter({'username': 'testuser'})

def test_build_filter_with_q_expression(user_query):
    q_expression = Q(username='testuser')
    clause, used_joins = user_query.build_filter(q_expression)
    assert clause is not None
    assert len(used_joins) == 0

def test_build_filter_with_non_conditional_expression_raises_type_error(user_query):
    expression = User.username  # This is not a conditional expression
    with pytest.raises(TypeError, match="Cannot filter against a non-conditional expression."):
        user_query.build_filter(expression)

def test_build_filter_with_empty_arg_raises_field_error(user_query):
    with pytest.raises(FieldError, match="Cannot parse keyword query %r" % ''):
        user_query.build_filter(('', 'value'))

def test_build_filter_with_valid_expression(user_query):
    clause, used_joins = user_query.build_filter(('username', 'testuser'))
    assert clause is not None
    assert len(used_joins) == 0

def test_build_filter_with_null_value(user_query):
    clause, used_joins = user_query.build_filter(('username', None))
    assert clause is not None
    assert len(used_joins) == 0

def test_build_filter_with_branch_negated(user_query):
    clause, used_joins = user_query.build_filter(('username', 'testuser'), branch_negated=True)
    assert clause is not None
    assert len(used_joins) == 0

def test_build_filter_with_invalid_join(user_query):
    with pytest.raises(FieldError, match="Joined field references are not permitted in this query"):
        user_query.build_filter(('profile__bio', 'some bio'), allow_joins=False)

def test_build_filter_with_okay_expression(user_query):
    clause, used_joins = user_query.build_filter(('email', 'test@example.com'))
    assert clause is not None
    assert len(used_joins) == 0