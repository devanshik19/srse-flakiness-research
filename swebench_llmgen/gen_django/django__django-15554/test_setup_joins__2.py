import pytest
from django.db import models
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

class TestQuerySetupJoins:

    @pytest.fixture
    def query(self):
        return Query(User)

    def test_setup_joins_basic(self, query):
        names = ['username']
        opts = User._meta
        alias = query.get_initial_alias()
        result = query.setup_joins(names, opts, alias)

        assert result is not None
        assert hasattr(result, 'final_field')
        assert hasattr(result, 'targets')
        assert hasattr(result, 'opts')
        assert hasattr(result, 'joins')
        assert hasattr(result, 'path')
        assert hasattr(result, 'transformer')

    def test_setup_joins_with_reverse_relation(self, query):
        names = ['groups']
        opts = User._meta
        alias = query.get_initial_alias()
        result = query.setup_joins(names, opts, alias, allow_many=False)

        assert result is not None
        assert hasattr(result, 'final_field')
        assert hasattr(result, 'targets')
        assert result.final_field is not None

    def test_setup_joins_invalid_field(self, query):
        names = ['invalid_field']
        opts = User._meta
        alias = query.get_initial_alias()

        with pytest.raises(FieldError):
            query.setup_joins(names, opts, alias)

    def test_setup_joins_with_transform(self, query):
        names = ['username__icontains']
        opts = User._meta
        alias = query.get_initial_alias()
        result = query.setup_joins(names, opts, alias)

        assert result is not None
        assert callable(result.transformer)

    def test_setup_joins_m2m(self, query):
        names = ['user_permissions']
        opts = User._meta
        alias = query.get_initial_alias()
        result = query.setup_joins(names, opts, alias)

        assert result is not None
        assert hasattr(result, 'final_field')
        assert hasattr(result, 'targets')
        assert result.final_field is not None
        assert isinstance(result.joins, list)