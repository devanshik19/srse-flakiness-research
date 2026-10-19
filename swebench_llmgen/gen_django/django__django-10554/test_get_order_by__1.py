import pytest
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.db.models.sql.compiler import SQLCompiler

@pytest.fixture
def user_query_set():
    return User.objects.all()

def test_get_order_by_default_ordering(user_query_set):
    query = user_query_set.query
    compiler = SQLCompiler(query, query.get_meta().db, using=None)
    sql_order_by = compiler.get_order_by()
    assert isinstance(sql_order_by, list)  # Check if the result is a list

def test_get_order_by_extra_ordering(user_query_set):
    query = user_query_set.query
    query.extra_order_by = ['username']  # Use an extra ORDER BY
    compiler = SQLCompiler(query, query.get_meta().db, using=None)
    sql_order_by = compiler.get_order_by()
    assert len(sql_order_by) > 0  # Ensure there's at least one order by clause

def test_get_order_by_no_ordering(user_query_set):
    query = user_query_set.query
    query.order_by = []  # No ordering set
    compiler = SQLCompiler(query, query.get_meta().db, using=None)
    sql_order_by = compiler.get_order_by()
    assert sql_order_by == []  # Expect an empty result for no ordering

def test_get_order_by_with_annotations(user_query_set):
    query = user_query_set.annotate(username_length=models.functions.Length('username')).order_by('username_length')
    compiler = SQLCompiler(query.query, query.get_meta().db, using=None)
    sql_order_by = compiler.get_order_by()
    assert any('username_length' in str(order) for order, _ in sql_order_by)  # Ensure annotation is included

def test_get_order_by_reverse_ordering(user_query_set):
    query = user_query_set.order_by('-date_joined')  # Reverse ordering
    compiler = SQLCompiler(query.query, query.get_meta().db, using=None)
    sql_order_by = compiler.get_order_by()
    assert any(order[0].descending for order in sql_order_by)  # Check that there's a descending order