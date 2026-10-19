import pytest
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.query import Query
from django.db.models.expressions import F

def test_output_field_single_select():
    user = User.objects.create(username='testuser')
    query = Query(model=User, alias_cols=None)
    query.select = [F('username')]
    
    # Testing output_field with a single select
    assert query.output_field() == user._meta.get_field('username')

def test_output_field_single_annotation_select():
    user = User.objects.create(username='testuser')
    query = Query(model=User, alias_cols=None)
    query.annotation_select = {'username_count': Count('username')}
    
    # Testing output_field with a single annotation select
    assert query.output_field() == Count('username').output_field

def test_output_field_multiple_selects():
    query = Query(model=User, alias_cols=None)
    query.select = [F('username'), F('email')]
    
    # Testing output_field with multiple selects should return None
    assert query.output_field() is None

def test_output_field_multiple_annotations():
    query = Query(model=User, alias_cols=None)
    query.annotation_select = {
        'username_count': Count('username'),
        'email_count': Count('email')
    }
    
    # Testing output_field with multiple annotations should also return None
    assert query.output_field() is None