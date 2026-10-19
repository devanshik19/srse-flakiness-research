import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query

@pytest.mark.parametrize(
    "filter_expr, can_reuse, names_with_path, expected_condition",
    [
        (("child__name", "foo"), set(), ["child"], "NOT IN"),
        (("child__name", User.objects.create(username='foo')), set(), ["child"], "NOT IN"),
        (("child__name", "foo"), {'child'}, ["child"], "NOT IN"),
    ]
)
def test_split_exclude(filter_expr, can_reuse, names_with_path, expected_condition):
    # Prepare an instance of Query
    query = Query(User)
    
    # Call the method under test
    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)
    
    # Check the expected structure of the condition
    assert hasattr(condition, 'children')
    assert expected_condition in str(condition)

    # Test if needed_inner is a boolean
    assert isinstance(needed_inner, bool)

def test_split_exclude_nullable_field():
    user = User.objects.create(username='testuser')
    filter_expr = ("username", user.username)
    can_reuse = set()
    names_with_path = []

    query = Query(User)
    query.add_filter(filter_expr)
    query.clear_ordering(True)

    # Call the method under test
    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)

    # Check to ensure that the condition is built correctly
    assert hasattr(condition, 'children')
    assert condition is not None
    assert len(condition.children) > 0  # Ensuring something was added to the condition

    # Check if it accommodates a scenario for nullable fields
    assert isinstance(needed_inner, bool)

def test_split_exclude_f_expression():
    user = User.objects.create(username='testuser', first_name='Foo')
    filter_expr = ("first_name", Q(first_name='Foo'))
    can_reuse = set()
    names_with_path = ['first_name']

    query = Query(User)
    
    # Call the method under test
    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)

    assert condition is not None
    assert hasattr(condition, 'children')
    assert len(condition.children) > 0  # Check that the condition got populated as expected