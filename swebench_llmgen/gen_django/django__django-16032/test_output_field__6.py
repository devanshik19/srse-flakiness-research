import pytest
from django.contrib.auth.models import User
from django.db.models import QuerySet, F
from django.db.models.sql.query import Query

# Create helper function to initialize Query with select and annotation_select
def create_query(*args, select=None, annotation_select=None):
    query = Query(User, alias_cols=None)
    query.select = select if select is not None else []
    query.annotation_select = annotation_select if annotation_select is not None else {}
    return query

def test_output_field_single_select_field():
    user = User.objects.create(username='testuser')
    query = create_query(select=[F('id')])
    assert query.output_field() == User._meta.get_field('id')

def test_output_field_single_annotation():
    user = User.objects.create(username='testuser')
    query = create_query(annotation_select={'user_count': Count('id')})
    assert query.output_field() == Count('id').output_field

def test_output_field_multiple_select_fields():
    user = User.objects.create(username='testuser')
    query = create_query(select=[F('id'), F('username')])
    assert query.output_field() is None

def test_output_field_multiple_annotation_select():
    user = User.objects.create(username='testuser')
    query = create_query(annotation_select={'user_count': Count('id'), 'user_age': F('age')})
    assert query.output_field() is None