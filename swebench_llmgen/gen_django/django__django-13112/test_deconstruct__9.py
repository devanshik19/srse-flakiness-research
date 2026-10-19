import pytest
from django.contrib.auth.models import User
from django.db.models import ForeignKey
from django.db.models.fields.related import RelatedField

class TestRelatedField(RelatedField):
    def __init__(self, related_name=None, related_query_name=None, limit_choices_to=None):
        self.remote_field = ForeignKey(User, on_delete=CASCADE)
        self.remote_field.related_name = related_name
        self.remote_field.related_query_name = related_query_name
        self.remote_field.limit_choices_to = limit_choices_to

def test_deconstruct_with_all_parameters():
    field = TestRelatedField(related_name='custom_related_name', related_query_name='custom_query_name', limit_choices_to={'is_active': True})
    name, path, args, kwargs = field.deconstruct()

    assert name is not None
    assert path is not None
    assert args == []
    assert kwargs['related_name'] == 'custom_related_name'
    assert kwargs['related_query_name'] == 'custom_query_name'
    assert kwargs['limit_choices_to'] == {'is_active': True}

def test_deconstruct_with_some_parameters():
    field = TestRelatedField(related_name=None, related_query_name='custom_query_name', limit_choices_to=None)
    name, path, args, kwargs = field.deconstruct()

    assert name is not None
    assert path is not None
    assert args == []
    assert 'related_name' not in kwargs
    assert kwargs['related_query_name'] == 'custom_query_name'
    assert 'limit_choices_to' not in kwargs

def test_deconstruct_with_no_parameters():
    field = TestRelatedField()
    name, path, args, kwargs = field.deconstruct()

    assert name is not None
    assert path is not None
    assert args == []
    assert 'related_name' not in kwargs
    assert 'related_query_name' not in kwargs
    assert 'limit_choices_to' not in kwargs