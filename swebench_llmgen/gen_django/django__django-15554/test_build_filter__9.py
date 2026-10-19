import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query
from django.core.exceptions import FieldError, TypeError

@pytest.mark.parametrize(
    "filter_expr, expected_exception",
    [
        ({"username": "testuser"}, FieldError),  # Invalid filter_expr type (dict)
        (Q(username="testuser"), None),          # Valid Q expression
        (User.username, TypeError),               # Non-conditional expression
        (("username", "testuser"), None),        # Valid tuple expression
        (("", "testuser"), FieldError),          # Invalid lookup (empty string)
    ]
)
def test_build_filter_exceptions(filter_expr, expected_exception):
    query = Query(User._meta)

    if expected_exception:
        with pytest.raises(expected_exception):
            query.build_filter(filter_expr)
    else:
        clause, used_joins = query.build_filter(filter_expr)
        assert clause is not None
        assert isinstance(clause, query.where.Node)

def test_build_filter_with_lookup():
    query = Query(User._meta)
    clause, used_joins = query.build_filter(('username', 'testuser'))
    
    assert len(clause.children) == 1
    assert clause.children[0].lhs.name == 'username'
    assert clause.children[0].rhs == 'testuser'
    assert clause.children[0].lookup_name == 'exact'

def test_build_filter_with_q_expression():
    query = Query(User._meta)
    q_expression = Q(username='testuser') | Q(email='test@example.com')
    clause, used_joins = query.build_filter(q_expression)
    
    assert len(clause.children) == 2
    
def test_build_filter_relationships():
    query = Query(User._meta)
    # Assuming there's a related field (here using a hypothetical 'profile' related field)
    # Replace 'profile' with an actual related field if applicable
    
    # clause, used_joins = query.build_filter(('profile__age', 30))
    # assert len(clause.children) == 1
    # assert 'profile' in str(clause)  # Check the clause string representation
    
def test_build_filter_null_condition():
    query = Query(User._meta)
    clause, used_joins = query.build_filter(('username', None))
    
    assert len(clause.children) == 1
    assert clause.children[0].lookup_name == 'isnull'
    assert clause.children[0].rhs is True