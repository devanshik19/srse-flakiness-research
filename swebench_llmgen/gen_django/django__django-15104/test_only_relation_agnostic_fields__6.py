import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector

class TestMigrationAutodetector:
    
    @pytest.fixture
    def autodetector(self):
        # Creating a MigrationAutodetector instance with arbitrary states
        return MigrationAutodetector(None, None, None)

    def test_only_relation_agnostic_fields(self, autodetector):
        # Prepare test fields
        fields = {
            'username': User._meta.get_field('username'),
            'email': User._meta.get_field('email'),
            'password': User._meta.get_field('password'),
            'groups': User._meta.get_field('groups'),
        }

        # Invoke the focal method
        result = autodetector.only_relation_agnostic_fields(fields)

        # Check if the results are as expected, ignoring the relation agnostic fields
        expected_fields_def = [
            autodetector.deep_deconstruct(field)
            for name, field in sorted(fields.items())
        ]

        # Ensure 'to' key is removed from expected_deconstruction for relation fields
        for deconstruction in expected_fields_def:
            if deconstruction[2].get('to') is not None:
                del deconstruction[2]['to']

        assert result == expected_fields_def