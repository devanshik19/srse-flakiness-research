import pytest
from django.contrib.auth.models import User
from django.db.models import ForeignKey
from django.db.models.fields.related import RelatedField

class TestRelatedField:
    def test_deconstruct_with_limit_choices_to(self):
        # Setup a RelatedField with limit_choices_to
        remote_field = ForeignKey(User, limit_choices_to={'is_active': True}, related_name='users')
        related_field = RelatedField()
        related_field.remote_field = remote_field
        
        name, path, args, kwargs = related_field.deconstruct()
        
        assert kwargs['limit_choices_to'] == {'is_active': True}
        assert 'related_name' in kwargs
        assert kwargs['related_name'] == 'users'

    def test_deconstruct_with_related_name(self):
        # Setup a RelatedField with related_name
        remote_field = ForeignKey(User, related_name='custom_related')
        related_field = RelatedField()
        related_field.remote_field = remote_field
        
        name, path, args, kwargs = related_field.deconstruct()
        
        assert 'related_name' in kwargs
        assert kwargs['related_name'] == 'custom_related'

    def test_deconstruct_with_related_query_name(self):
        # Setup a RelatedField with related_query_name
        remote_field = ForeignKey(User, related_query_name='custom_query')
        related_field = RelatedField()
        related_field.remote_field = remote_field
        
        name, path, args, kwargs = related_field.deconstruct()
        
        assert 'related_query_name' in kwargs
        assert kwargs['related_query_name'] == 'custom_query'

    def test_deconstruct_without_additional_fields(self):
        # Setup a RelatedField with no additional fields
        remote_field = ForeignKey(User)
        related_field = RelatedField()
        related_field.remote_field = remote_field
        
        name, path, args, kwargs = related_field.deconstruct()
        
        assert 'limit_choices_to' not in kwargs
        assert 'related_name' not in kwargs
        assert 'related_query_name' not in kwargs