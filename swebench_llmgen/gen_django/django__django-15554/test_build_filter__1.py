import pytest
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import FieldError, TypeError
from django.db.models.sql.query import Query

@pytest.fixture
def query_instance():
    return Query(User.objects.all().query)

def test_build_filter_with_dict(query_instance):
    with pytest.raises(FieldError, match="Cannot parse keyword query as dict"):
        query_instance.build_filter({"username": "testuser"})

def test_build_filter_with_q_expression(query_instance):
    q_expr = Q(username='testuser')
    where_node, used_joins = query_instance.build_filter(q_expr)
    assert isinstance(where_node, list)
    assert used_joins == []

def test_build_filter_with_non_conditional_expression(query_instance):
    class NonConditionalExpr:
        conditional = False

        def resolve_expression(self, query, allow_joins=True):
            pass

    non_conditional_expr = NonConditionalExpr()
    with pytest.raises(TypeError, match="Cannot filter against a non-conditional expression."):
        query_instance.build_filter(non_conditional_expr)

def test_build_filter_with_empty_arg(query_instance):
    with pytest.raises(FieldError, match="Cannot parse keyword query None"):
        query_instance.build_filter((None, "testvalue"))

def test_build_filter_with_no_reffed_expression(query_instance):
    filter_expr = ('username', 'testuser')
    where_node, used_joins = query_instance.build_filter(filter_expr)
    assert isinstance(where_node, list)
    assert used_joins == []

def test_build_filter_with_joined_field_references(query_instance):
    with pytest.raises(FieldError, match="Joined field references are not permitted in this query"):
        query_instance.build_filter(('related_field__username', 'testuser'))

def test_build_filter_with_isnull_condition(query_instance):
    filter_expr = ('username', None)
    where_node, _ = query_instance.build_filter(filter_expr)
    assert len(where_node) == 1
    assert where_node[0].lookup_name == 'isnull'
    assert where_node[0].rhs

def test_build_filter_with_nullable_condition(query_instance):
    # Test with a nullable column, for illustration since User.username is not nullable.
    filter_expr = ('username', 'non_existing_user')
    where_node, used_joins = query_instance.build_filter(filter_expr)
    assert isinstance(where_node, list)
    assert used_joins == []

def test_build_filter_with_relation(query_instance):
    # Assuming username is not a relation but testing for proper build.
    filter_expr = ('last_login', None)
    where_node, used_joins = query_instance.build_filter(filter_expr)
    assert isinstance(where_node, list)
    assert used_joins == []