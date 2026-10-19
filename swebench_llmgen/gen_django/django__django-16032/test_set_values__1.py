import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def query_instance():
    user_model = User
    return Query(user_model)

def test_set_values_with_valid_fields(query_instance):
    fields = ['username', 'email']
    query_instance.set_values(fields)
    
    assert query_instance.values_select == ('username', 'email')
    assert query_instance.select_related is False
    assert len(query_instance.extra_select_mask) == 0
    assert len(query_instance.annotation_select_mask) == 0

def test_set_values_with_extra_fields(query_instance):
    query_instance.extra_select = ['is_active']
    query_instance.annotations = {}
    fields = ['username', 'is_active']
    query_instance.set_values(fields)
    
    assert query_instance.values_select == ('username', 'is_active')
    assert query_instance.extra_select_mask == ['is_active']

def test_set_values_with_annotations(query_instance):
    query_instance.extra_select = {}
    query_instance.annotations = {'new_annotation': 'annotation_value'}
    fields = ['username', 'new_annotation']
    query_instance.set_values(fields)
    
    assert query_instance.values_select == ('username', 'new_annotation')
    assert query_instance.annotation_select_mask == ['new_annotation']

def test_set_values_with_empty_fields(query_instance):
    fields = []
    query_instance.set_values(fields)
    
    assert query_instance.values_select == tuple(f.attname for f in User._meta.concrete_fields)
    assert len(query_instance.extra_select_mask) == 0
    assert len(query_instance.annotation_select_mask) == 0

def test_set_values_group_by_true(query_instance):
    query_instance.group_by = True
    fields = ['username']
    query_instance.set_values(fields)
    
    assert query_instance.group_by is False
    assert query_instance.values_select == ('username',)
    
def test_set_values_with_group_by_annotations(query_instance):
    query_instance.group_by = ['new_annotation']
    query_instance.annotations = {'new_annotation': 'annotation_value'}
    fields = ['username']
    query_instance.set_values(fields)
    
    assert query_instance.group_by == (query_instance.annotations['new_annotation'],)
    assert query_instance.values_select == ('username',)