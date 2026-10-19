import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.exceptions import FieldError, TypeError
from django.db.models.sql.query import Query

@pytest.fixture
def query():
    # Create an instance of the Query class for the User model
    return Query(User)

def test_build_filter_invalid_dict(query):
    with pytest.raises(FieldError, match="Cannot parse keyword query as dict"):
        query.build_filter({'username': 'testuser'})

def test_build_filter_invalid_non_conditional_expression(query):
    class NonConditionalExpression:
        pass
    
    with pytest.raises(TypeError, match="Cannot filter against a non-conditional expression."):
        query.build_filter(NonConditionalExpression())

def test_build_filter_with_q_object(query):
    q = Q(username='testuser')
    clause, used_joins = query.build_filter(q)
    assert clause is not None
    assert used_joins == set()

def test_build_filter_with_expression(query):
    clause, used_joins = query.build_filter(('username', 'testuser'))
    assert clause is not None
    assert used_joins == set()

def test_build_filter_empty_arg(query):
    with pytest.raises(FieldError, match="Cannot parse keyword query None"):
        query.build_filter((None, 'testuser'))

def test_build_filter_valid_join(query):
    # Assume a User model instance is available for filtering
    User.objects.create(username='testuser', password='password123')
    clause, used_joins = query.build_filter(('username', 'testuser'))
    assert clause is not None

def test_build_filter_negated_conditions(query):
    clause, used_joins = query.build_filter(('username__isnull', True), current_negated=True)
    assert clause is not None

def test_build_filter_with_non_filterable_expression(query):
    # This should raise an exception if a non-filterable expression is used
    with pytest.raises(FieldError):
        query.build_filter(('nonexistent_field', 'value'))