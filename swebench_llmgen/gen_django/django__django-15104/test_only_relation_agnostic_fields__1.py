import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector

class TestMigrationAutodetector:
    
    @pytest.fixture
    def autodetector(self):
        return MigrationAutodetector(from_state=None, to_state=None, questioner=None)

    def test_only_relation_agnostic_fields_no_related_fields(self, autodetector):
        fields = {
            'username': User._meta.get_field('username'),
            'email': User._meta.get_field('email'),
        }
        result = autodetector.only_relation_agnostic_fields(fields)
        expected = [
            autodetector.deep_deconstruct(User._meta.get_field('username')),
            autodetector.deep_deconstruct(User._meta.get_field('email')),
        ]
        assert result == expected

    def test_only_relation_agnostic_fields_with_related_field(self, autodetector):
        # Create a related model
        class Profile(models.Model):
            user = models.OneToOneField(User, on_delete=models.CASCADE)
            bio = models.TextField()

        fields = {
            'user': Profile._meta.get_field('user'),
            'bio': Profile._meta.get_field('bio'),
        }
        result = autodetector.only_relation_agnostic_fields(fields)
        
        # Deep deconstruction should remove 'to' from related field
        user_deconstruct = autodetector.deep_deconstruct(Profile._meta.get_field('user'))
        user_deconstruct[2].pop('to', None)  # Remove 'to' from the deconstruction
        
        expected = [
            user_deconstruct,
            autodetector.deep_deconstruct(Profile._meta.get_field('bio')),
        ]
        
        assert result == expected

    def test_only_relation_agnostic_fields_empty(self, autodetector):
        fields = {}
        result = autodetector.only_relation_agnostic_fields(fields)
        assert result == []