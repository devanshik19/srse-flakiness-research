import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import RelatedField

class TestRelatedField(RelatedField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.remote_field = kwargs.get('remote_field', None)

@pytest.fixture
def related_field_with_attributes():
    class RemoteField:
        limit_choices_to = Q(is_active=True)
        related_name = 'user_related'
        related_query_name = 'user_query'

    return TestRelatedField(remote_field=RemoteField())

def test_deconstruct_with_limit_choices_and_related_name(related_field_with_attributes):
    name, path, args, kwargs = related_field_with_attributes.deconstruct()
    assert kwargs['limit_choices_to'] == related_field_with_attributes.remote_field.limit_choices_to
    assert kwargs['related_name'] == related_field_with_attributes.remote_field.related_name
    assert 'related_query_name' not in kwargs  # Assert not present for this test

def test_deconstruct_with_related_query_name(related_field_with_attributes):
    related_field_with_attributes.remote_field.related_query_name = 'custom_query'
    name, path, args, kwargs = related_field_with_attributes.deconstruct()
    assert kwargs['related_query_name'] == related_field_with_attributes.remote_field.related_query_name

def test_deconstruct_with_no_attributes():
    no_attr_related_field = TestRelatedField()
    name, path, args, kwargs = no_attr_related_field.deconstruct()
    assert 'limit_choices_to' not in kwargs
    assert 'related_name' not in kwargs
    assert 'related_query_name' not in kwargs