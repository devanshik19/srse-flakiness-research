import pytest
from django.db.models.sql.query import Query
from django.contrib.auth.models import User
from django.db.models import F

def test_output_field_single_select():
    query = Query(User)
    query.select = [F('username')]
    expected_output_field = User._meta.get_field('username')
    assert query.output_field() == expected_output_field

def test_output_field_single_annotation_select():
    query = Query(User)
    query.annotation_select = {'username_count': Count('username')}
    expected_output_field = query.annotation_select['username_count'].output_field
    assert query.output_field() == expected_output_field

def test_output_field_multiple_selects():
    query = Query(User)
    query.select = [F('username'), F('email')]
    query.annotation_select = {}
    assert query.output_field() is None

def test_output_field_multiple_annotation_selects():
    query = Query(User)
    query.annotation_select = {
        'username_count': Count('username'),
        'email_count': Count('email')
    }
    assert query.output_field() == query.annotation_select['username_count'].output_field

def test_output_field_no_selects():
    query = Query(User)
    query.select = []
    query.annotation_select = {}
    assert query.output_field() is None