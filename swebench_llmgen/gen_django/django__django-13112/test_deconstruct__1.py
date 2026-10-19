import pytest
from django.contrib.auth.models import User
from django.db import models

class RelatedField(models.Field):
    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.remote_field.limit_choices_to:
            kwargs['limit_choices_to'] = self.remote_field.limit_choices_to
        if self.remote_field.related_name is not None:
            kwargs['related_name'] = self.remote_field.related_name
        if self.remote_field.related_query_name is not None:
            kwargs['related_query_name'] = self.remote_field.related_query_name
        return name, path, args, kwargs

# Sample RemoteField class for testing
class SampleRemoteField:
    def __init__(self, limit_choices_to=None, related_name=None, related_query_name=None):
        self.limit_choices_to = limit_choices_to
        self.related_name = related_name
        self.related_query_name = related_query_name

@pytest.fixture
def related_field_with_attrs():
    remote_field = SampleRemoteField(limit_choices_to={'is_active': True}, related_name='users', related_query_name='active_users')
    field = RelatedField()
    field.remote_field = remote_field
    return field

@pytest.fixture
def related_field_without_attrs():
    remote_field = SampleRemoteField()
    field = RelatedField()
    field.remote_field = remote_field
    return field

def test_deconstruct_with_attrs(related_field_with_attrs):
    name, path, args, kwargs = related_field_with_attrs.deconstruct()
    assert 'limit_choices_to' in kwargs
    assert kwargs['limit_choices_to'] == {'is_active': True}
    assert 'related_name' in kwargs
    assert kwargs['related_name'] == 'users'
    assert 'related_query_name' in kwargs
    assert kwargs['related_query_name'] == 'active_users'

def test_deconstruct_without_attrs(related_field_without_attrs):
    name, path, args, kwargs = related_field_without_attrs.deconstruct()
    assert 'limit_choices_to' not in kwargs
    assert 'related_name' not in kwargs
    assert 'related_query_name' not in kwargs