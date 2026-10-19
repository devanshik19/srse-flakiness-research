import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query
from django.core.exceptions import FieldError, EmptyResultSet

class TestQueryBuildFilter:
    def setup_method(self):
        self.query = Query(model=User)

    def test_build_filter_with_dict_raises_field_error(self):
        with pytest.raises(FieldError, match="Cannot parse keyword query as dict"):
            self.query.build_filter({'username': 'testuser'})

    def test_build_filter_with_q_object(self):
        q = Q(username='testuser')
        where_node, used_joins = self.query.build_filter(q)
        assert isinstance(where_node, WhereNode)
        assert len(used_joins) == 0

    def test_build_filter_with_non_conditional_expression_raises_type_error(self):
        with pytest.raises(TypeError, match="Cannot filter against a non-conditional expression."):
            filter_expr = User.username  # Non-conditional, as it's not an expression
            self.query.build_filter(filter_expr)

    def test_build_filter_with_valid_keyword_query(self):
        where_node, used_joins = self.query.build_filter(('username', 'testuser'))
        assert isinstance(where_node, WhereNode)
        assert len(used_joins) == 0

    def test_build_filter_with_empty_arg_raises_field_error(self):
        with pytest.raises(FieldError, match="Cannot parse keyword query None"):
            self.query.build_filter((None, 'testuser'))

    def test_build_filter_with_reffed_expression(self):
        # Assuming 'username' is a field on User model
        where_node, used_joins = self.query.build_filter(('username__exact', 'testuser'))
        assert isinstance(where_node, WhereNode)
        assert len(used_joins) == 0

    def test_build_filter_with_nested_joins(self):
        with pytest.raises(FieldError, match="Joined field references are not permitted in this query"):
            self.query.build_filter(('profile__bio', 'Some bio text'), allow_joins=False)

    def test_build_filter_with_nullable_column(self):
        User.objects.create(username='testuser')  # Create a user for lookup
        where_node, used_joins = self.query.build_filter(('username', None))
        assert isinstance(where_node, WhereNode)
        assert len(used_joins) == 0