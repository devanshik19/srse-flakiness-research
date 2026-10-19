import pytest
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query
from django.db.models.expressions import Value

# Helper function to create a QuerySet with ordering
def create_ordered_queryset(order_by):
    qs = User.objects.all()
    qs = qs.order_by(*order_by)
    return qs

# Create a new class to test different scenarios for SQLCompiler
class TestSQLCompiler:

    @pytest.fixture
    def setup_query(self):
        # Create a basic query
        query = Query(model=User)
        query.order_by = ['username']
        query.extra_order_by = []
        query.default_ordering = True
        query.annotations = {}
        query.extra = {}
        compiler = SQLCompiler(query, None, None)
        return query, compiler

    def test_get_order_by_with_default_ordering(self, setup_query):
        query, compiler = setup_query
        order_by = compiler.get_order_by()
        assert order_by[0][0].name == 'username'
        assert len(order_by) == 1

    def test_get_order_by_with_extra_ordering(self, setup_query):
        query, compiler = setup_query
        query.extra_order_by = ['email']
        order_by = compiler.get_order_by()
        assert order_by[0][0].name == 'email'
        assert len(order_by) == 1

    def test_get_order_by_with_no_ordering(self, setup_query):
        query, compiler = setup_query
        query.order_by = []
        query.default_ordering = False
        order_by = compiler.get_order_by()
        assert order_by == []

    def test_get_order_by_with_annotations(self, setup_query):
        query, compiler = setup_query
        query.annotations = {'annotated_username': Value('username')}
        query.order_by = ['annotated_username']
        order_by = compiler.get_order_by()
        assert order_by[0][0].name == 'annotated_username'
        assert len(order_by) == 1

    def test_get_order_by_with_random(self, setup_query):
        query, compiler = setup_query
        query.order_by = ['?']
        order_by = compiler.get_order_by()
        assert isinstance(order_by[0][0], Value)  # Expecting a Random instance

    def test_get_order_by_combined_ordering(self, setup_query):
        query, compiler = setup_query
        query.order_by = ['username', '-email']
        order_by = compiler.get_order_by()
        assert order_by[0][0].name == 'username'
        assert order_by[1][0].name == 'email'
        assert order_by[1][0].descending is True
        assert len(order_by) == 2