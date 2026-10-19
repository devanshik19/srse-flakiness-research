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

# Assume this test class is designed to test the RelatedField's deconstruct method
class TestRelatedField:
    def test_deconstruct_with_limit_choices_to(self):
        remote_field = type('RemoteField', (), {
            'limit_choices_to': Q(id=1),
            'related_name': 'related_user',
            'related_query_name': 'user_query'
        })()

        related_field = RelatedField()
        related_field.remote_field = remote_field
        
        name, path, args, kwargs = related_field.deconstruct()
        
        assert kwargs['limit_choices_to'] == remote_field.limit_choices_to
        assert kwargs['related_name'] == remote_field.related_name
        assert kwargs['related_query_name'] == remote_field.related_query_name

    def test_deconstruct_without_limit_choices(self):
        remote_field = type('RemoteField', (), {
            'limit_choices_to': None,
            'related_name': None,
            'related_query_name': None
        })()

        related_field = RelatedField()
        related_field.remote_field = remote_field
        
        name, path, args, kwargs = related_field.deconstruct()
        
        assert 'limit_choices_to' not in kwargs
        assert 'related_name' not in kwargs
        assert 'related_query_name' not in kwargs