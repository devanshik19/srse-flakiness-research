import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_output_field_single_select():
    user = User.objects.create(username='testuser')
    query = Query(model=User, alias_cols=[('id', 'users_id')])
    query.select = [user]
    
    assert query.output_field() == user

def test_output_field_single_annotation_select():
    user = User.objects.create(username='testuser')
    query = Query(model=User, alias_cols=[('id', 'users_id')])
    query.annotation_select = {'count': Count('id')}
    
    assert query.output_field() == Count('id')

def test_output_field_multiple_selects():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    query = Query(model=User, alias_cols=[('id', 'users_id')])
    query.select = [user1, user2]
    
    assert query.output_field() is None

def test_output_field_multiple_annotations():
    user = User.objects.create(username='testuser')
    query = Query(model=User, alias_cols=[('id', 'users_id')])
    query.annotation_select = {'count1': Count('id'), 'count2': Count('username')}
    
    result = query.output_field()
    assert result is not None
    assert isinstance(result, Count)
    assert result.name in ['count1', 'count2']