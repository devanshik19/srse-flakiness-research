import pytest
from django.contrib.auth.models import User
from django.db import models


class RelatedField(models.Field):
    remote_field = None

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.remote_field.limit_choices_to:
            kwargs['limit_choices_to'] = self.remote_field.limit_choices_to
        if self.remote_field.related_name is not None:
            kwargs['related_name'] = self.remote_field.related_name
        if self.remote_field.related_query_name is not None:
            kwargs['related_query_name'] = self.remote_field.related_query_name
        return name, path, args, kwargs


class MockRemoteField:
    def __init__(self, limit_choices_to=None, related_name=None, related_query_name=None):
        self.limit_choices_to = limit_choices_to
        self.related_name = related_name
        self.related_query_name = related_query_name


@pytest.fixture
def related_field_with_limit_choices():
    field = RelatedField()
    field.remote_field = MockRemoteField(limit_choices_to={'is_active': True})
    return field


@pytest.fixture
def related_field_with_related_name():
    field = RelatedField()
    field.remote_field = MockRemoteField(related_name='related_users')
    return field


@pytest.fixture
def related_field_with_related_query_name():
    field = RelatedField()
    field.remote_field = MockRemoteField(related_query_name='active_users')
    return field


def test_deconstruct_with_limit_choices(related_field_with_limit_choices):
    name, path, args, kwargs = related_field_with_limit_choices.deconstruct()
    assert kwargs['limit_choices_to'] == {'is_active': True}
    assert 'related_name' not in kwargs
    assert 'related_query_name' not in kwargs


def test_deconstruct_with_related_name(related_field_with_related_name):
    name, path, args, kwargs = related_field_with_related_name.deconstruct()
    assert kwargs['related_name'] == 'related_users'
    assert 'limit_choices_to' not in kwargs
    assert 'related_query_name' not in kwargs


def test_deconstruct_with_related_query_name(related_field_with_related_query_name):
    name, path, args, kwargs = related_field_with_related_query_name.deconstruct()
    assert kwargs['related_query_name'] == 'active_users'
    assert 'limit_choices_to' not in kwargs
    assert 'related_name' not in kwargs


def test_deconstruct_with_all_fields(related_field_with_limit_choices):
    related_field_with_limit_choices.remote_field.related_name = 'related_users'
    related_field_with_limit_choices.remote_field.related_query_name = 'active_users'
    
    name, path, args, kwargs = related_field_with_limit_choices.deconstruct()
    assert kwargs['limit_choices_to'] == {'is_active': True}
    assert kwargs['related_name'] == 'related_users'
    assert kwargs['related_query_name'] == 'active_users'