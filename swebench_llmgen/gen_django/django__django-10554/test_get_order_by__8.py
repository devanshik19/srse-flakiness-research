import pytest
from django.db.models import F
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query
from django.contrib.auth.models import User

class TestSQLCompilerGetOrderBy:
    @pytest.fixture
    def setup_query(self):
        # Create a new query instance and a compiler for our tests
        query = Query(User)
        compiler = SQLCompiler(query=query, connection=None, using=None)
        return compiler

    def test_get_order_by_with_extra_order_by(self, setup_query):
        setup_query.query.extra_order_by = ['-username']
        result = setup_query.get_order_by()
        assert len(result) == 1
        assert result[0][0].expression == 'username'
        assert result[0][1] == ('-username', [], False)

    def test_get_order_by_with_default_ordering(self, setup_query):
        setup_query.query.default_ordering = True
        setup_query.query.order_by = ['username']
        result = setup_query.get_order_by()
        assert len(result) == 1
        assert result[0][0].expression == 'username'
        assert result[0][1] == ('username', [], False)

    def test_get_order_by_with_no_ordering(self, setup_query):
        setup_query.query.default_ordering = False
        setup_query.query.order_by = []
        assert setup_query.get_order_by() == []

    def test_get_order_by_with_meta_ordering(self, setup_query):
        setup_query.query.default_ordering = True
        setup_query.query.order_by = []
        setup_query.query.get_meta = lambda: type('Meta', (), {'ordering': ['email']})()
        result = setup_query.get_order_by()
        assert len(result) == 1
        assert result[0][0].expression == 'email'
        assert result[0][1] == ('email', [], False)

    def test_get_order_by_with_random(self, setup_query):
        setup_query.query.order_by = ['?']
        result = setup_query.get_order_by()
        assert len(result) == 1
        assert isinstance(result[0][0], OrderBy) and isinstance(result[0][0].expression, Random)

    def test_get_order_by_with_annotation(self, setup_query):
        setup_query.query.annotations = {'ordered_username': F('username')}
        setup_query.query.order_by = ['ordered_username']
        result = setup_query.get_order_by()
        assert len(result) == 1
        assert result[0][0].expression == 'ordered_username'
        assert result[0][1] == ('ordered_username', [], False)