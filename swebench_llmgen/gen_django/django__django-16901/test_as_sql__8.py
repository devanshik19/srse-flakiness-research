import pytest
from django.contrib.auth.models import User
from django.db.models.sql.where import WhereNode

def test_as_sql_with_empty_children():
    wn = WhereNode(children=[], connector='AND')
    with pytest.raises(FullResultSet):
        wn.as_sql(None, None)

def test_as_sql_with_full_children():
    wn = WhereNode(children=[User.objects.filter(username='test_user')], connector='AND')
    sql, params = wn.as_sql(None, None)
    assert sql  # Ensure some SQL is generated
    assert params == []  # No parameters should be needed for default user query

def test_as_sql_with_negated_empty_children():
    wn = WhereNode(children=[], connector='AND', negated=True)
    with pytest.raises(EmptyResultSet):
        wn.as_sql(None, None)

def test_as_sql_with_multiple_children():
    wn = WhereNode(children=[User.objects.filter(username='test_user'), User.objects.filter(username='test_user_2')], connector='OR')
    sql, params = wn.as_sql(None, None)
    assert sql  # Ensure some SQL is generated
    assert 'OR' in sql  # Ensure the connector is correctly used

def test_as_sql_with_xor_not_supported():
    wn = WhereNode(children=[User.objects.filter(username='test_user')], connector='XOR')
    sql, params = wn.as_sql(None, None)
    assert sql  # Ensure some SQL is generated

def test_as_sql_with_only_negated_children():
    wn = WhereNode(children=[User.objects.filter(username='non_existent_user')], connector='AND', negated=True)
    sql, params = wn.as_sql(None, None)
    assert sql  # Ensure it generates SQL even with negation
    assert params == []  # No parameters should be needed for query

def test_as_sql_with_combined_conditions():
    wn = WhereNode(children=[
        User.objects.filter(username='test_user'),
        User.objects.filter(username='test_user_2')
    ], connector='AND')

    sql, params = wn.as_sql(None, None)
    assert sql  # Ensure some SQL is generated
    assert 'AND' in sql  # Ensure the connector is correctly used