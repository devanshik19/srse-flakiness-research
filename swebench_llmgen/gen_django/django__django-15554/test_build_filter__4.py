import pytest
from django.contrib.auth.models import User
from django.core.exceptions import FieldError, TypeError
from django.db.models import Q
from django.db.models.sql.query import Query

class TestQueryBuildFilter:

    @pytest.fixture
    def query(self):
        return Query()  # Create a new instance of the Query class

    def test_build_filter_with_dict(self, query):
        with pytest.raises(FieldError, match="Cannot parse keyword query as dict"):
            query.build_filter({'username': 'test'})

    def test_build_filter_with_q_object(self, query):
        q_object = Q(username='test')
        clause, used_joins = query.build_filter(q_object)
        assert clause is not None
        assert used_joins == []

    def test_build_filter_with_non_conditional_expression(self, query):
        class NonConditional:
            conditional = False
            
            def resolve_expression(self, query, allow_joins=True):
                return self

        non_conditional = NonConditional()
        with pytest.raises(TypeError, match="Cannot filter against a non-conditional expression."):
            query.build_filter(non_conditional)

    def test_build_filter_with_valid_expression(self, query):
        user = User.objects.create_user(username='testuser', password='password')
        clause, used_joins = query.build_filter(('username', 'testuser'))
        assert clause is not None
        assert user.username == 'testuser'

    def test_build_filter_with_empty_arg(self, query):
        with pytest.raises(FieldError, match="Cannot parse keyword query %r" % ''):
            query.build_filter(('', 'value'))

    def test_build_filter_with_join_fields_not_permitted(self, query):
        with pytest.raises(FieldError, match="Joined field references are not permitted in this query"):
            query.build_filter(('related_model__field', 'value'), allow_joins=False)

    def test_build_filter_with_invalid_lookup(self, query):
        user = User.objects.create_user(username='testuser', password='password')
        lookup_field = 'username__invalid_lookup'
        with pytest.raises(FieldError, match="Related Field got invalid lookup: username__invalid_lookup"):
            query.build_filter((lookup_field, 'testuser'))

    def test_build_filter_with_nullable_value(self, query):
        user = User.objects.create_user(username='testuser', password='password')
        clause, used_joins = query.build_filter(('username', None))
        assert clause is not None
        assert len(clause.children) == 1