import pytest
from django.db import models
from django.contrib.auth.models import User


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


def test_deconstruct_with_limit_choices_to_and_related_names():
    field = RelatedField()
    field.remote_field = type('RemoteField', (), {
        'limit_choices_to': Q(is_active=True),
        'related_name': 'related_users',
        'related_query_name': 'user_query'
    })()

    name, path, args, kwargs = field.deconstruct()

    assert kwargs['limit_choices_to'] == Q(is_active=True)
    assert kwargs['related_name'] == 'related_users'
    assert kwargs['related_query_name'] == 'user_query'


def test_deconstruct_without_limit_choices_to_and_related_names():
    field = RelatedField()
    field.remote_field = type('RemoteField', (), {
        'limit_choices_to': None,
        'related_name': None,
        'related_query_name': None
    })()

    name, path, args, kwargs = field.deconstruct()

    assert 'limit_choices_to' not in kwargs
    assert 'related_name' not in kwargs
    assert 'related_query_name' not in kwargs