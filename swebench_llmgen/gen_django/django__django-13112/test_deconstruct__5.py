import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import RelatedField

class TestRelatedField(RelatedField):
    def __init__(self, **kwargs):
        self.remote_field = kwargs.get('remote_field', None)
        super().__init__(**kwargs)

@pytest.fixture
def related_field_with_values():
    remote_field = type('RemoteField', (), {})()
    remote_field.limit_choices_to = Q(is_active=True)
    remote_field.related_name = 'test_related'
    remote_field.related_query_name = 'test_query'
    return TestRelatedField(remote_field=remote_field)

@pytest.fixture
def related_field_without_values():
    remote_field = type('RemoteField', (), {})()
    remote_field.limit_choices_to = None
    remote_field.related_name = None
    remote_field.related_query_name = None
    return TestRelatedField(remote_field=remote_field)

def test_deconstruct_with_values(related_field_with_values):
    name, path, args, kwargs = related_field_with_values.deconstruct()
    assert kwargs['limit_choices_to'] == related_field_with_values.remote_field.limit_choices_to
    assert kwargs['related_name'] == related_field_with_values.remote_field.related_name
    assert kwargs['related_query_name'] == related_field_with_values.remote_field.related_query_name

def test_deconstruct_without_values(related_field_without_values):
    name, path, args, kwargs = related_field_without_values.deconstruct()
    assert 'limit_choices_to' not in kwargs
    assert 'related_name' not in kwargs
    assert 'related_query_name' not in kwargs