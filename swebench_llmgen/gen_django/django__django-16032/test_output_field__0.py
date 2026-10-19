import pytest
from django.db.models import QuerySet
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_output_field_single_select():
    user = User.objects.create(username='testuser')
    query = Query(model=User, alias_cols=())
    query.select = [user]
    
    assert query.output_field() == user._meta.get_field('username')

def test_output_field_single_annotation_select():
    user = User.objects.create(username='testuser')
    query = Query(model=User, alias_cols=())
    query.annotation_select = {'username_count': Count('username')}
    
    assert query.output_field() == query.annotation_select['username_count'].output_field

def test_output_field_multiple_selects():
    user1 = User.objects.create(username='testuser1')
    user2 = User.objects.create(username='testuser2')
    query = Query(model=User, alias_cols=())
    query.select = [user1, user2]
    
    assert query.output_field() is None

def test_output_field_multiple_annotation_selects():
    user = User.objects.create(username='testuser')
    query = Query(model=User, alias_cols=())
    query.annotation_select = {
        'username_count': Count('username'),
        'email_count': Count('email'),
    }
    
    assert query.output_field() == query.annotation_select['username_count'].output_field