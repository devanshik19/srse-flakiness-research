import pytest
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def query_with_select():
    # Create a Query instance with a select clause containing a simple mapped field
    user_model = User._meta
    # This mimics what Django would have in a real scenario for select
    query = Query(model=user_model, alias_cols={}) 
    query.select = [F('username')]
    return query

@pytest.fixture
def query_with_annotation():
    # Create a Query instance with an annotation
    user_model = User._meta
    query = Query(model=user_model, alias_cols={})
    query.annotation_select = {'annotated_field': F('username')}
    return query

def test_output_field_with_single_select(query_with_select):
    assert query_with_select.output_field() == query_with_select.select[0].field

def test_output_field_with_single_annotation(query_with_annotation):
    assert query_with_annotation.output_field() == query_with_annotation.annotation_select['annotated_field'].output_field

def test_output_field_with_no_select_or_annotation():
    user_model = User._meta
    query = Query(model=user_model, alias_cols={})
    query.select = []
    query.annotation_select = {}
    assert query.output_field() is None