import pytest
from django.contrib.auth.models import User
from django.db.models.sql.where import WhereNode, SubqueryConstraint, AND, OR
from django.db.models.fields.related_lookups import RelatedIn


def test_as_sql_with_multicolumn_lookup():
    lhs = User._meta.get_field('username')  # Adjust to a valid field for example
    rhs = ['user1', 'user2']
    related_in = RelatedIn(lhs, rhs)

    class MockCompiler:
        pass

    class MockConnection:
        pass

    sql, params = related_in.as_sql(MockCompiler(), MockConnection())
    assert isinstance(sql, str)
    assert 'WHERE' in sql  # Ensure SQL part has WHERE clause
    assert all(value in params for value in rhs)  # Ensure correct params are passed


def test_as_sql_with_subquery_constraint():
    lhs = User._meta.get_field('username')  # Example field
    rhs = User.objects.filter(is_active=True)  # Using a subquery
    related_in = RelatedIn(lhs, rhs)

    class MockCompiler:
        pass

    class MockConnection:
        pass

    sql, params = related_in.as_sql(MockCompiler(), MockConnection())
    assert isinstance(sql, str)
    assert 'WHERE' in sql


def test_as_sql_with_primary_key_case():
    lhs = User._meta.get_field('email')  # Example field that is not PK
    rhs = User.objects.filter(is_staff=True)  # Another queryset
    related_in = RelatedIn(lhs, rhs)

    class MockCompiler:
        pass

    class MockConnection:
        pass

    sql, params = related_in.as_sql(MockCompiler(), MockConnection())
    assert isinstance(sql, str)
    assert 'WHERE' in sql