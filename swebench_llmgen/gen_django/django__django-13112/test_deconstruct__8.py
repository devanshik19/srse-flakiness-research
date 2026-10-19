import pytest
from django.db.models import ForeignKey, OneToOneField
from django.contrib.auth.models import User
from django.db import models

class RelatedField(ForeignKey):
    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.remote_field.limit_choices_to:
            kwargs['limit_choices_to'] = self.remote_field.limit_choices_to
        if self.remote_field.related_name is not None:
            kwargs['related_name'] = self.remote_field.related_name
        if self.remote_field.related_query_name is not None:
            kwargs['related_query_name'] = self.remote_field.related_query_name
        return name, path, args, kwargs

@pytest.mark.django_db
def test_deconstruct():
    # Arrange
    limit_choices_to = Q(is_active=True)
    related_name = 'user_profile'
    related_query_name = 'profile'
    related_field = RelatedField(User, related_name=related_name, 
                                 related_query_name=related_query_name,
                                 limit_choices_to=limit_choices_to)

    # Act
    name, path, args, kwargs = related_field.deconstruct()

    # Assert
    assert name is not None
    assert path == 'django.contrib.auth.models.User'
    assert args == []
    assert kwargs['limit_choices_to'] == limit_choices_to
    assert kwargs['related_name'] == related_name
    assert kwargs['related_query_name'] == related_query_name

    # Test with default values (no limit_choices_to, related_name, related_query_name)
    default_field = RelatedField(User)
    name, path, args, kwargs = default_field.deconstruct()
    assert 'limit_choices_to' not in kwargs
    assert 'related_name' not in kwargs
    assert 'related_query_name' not in kwargs