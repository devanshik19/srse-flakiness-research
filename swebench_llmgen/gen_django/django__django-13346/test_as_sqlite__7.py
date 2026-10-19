import json
import pytest
from django.db import connections
from django.contrib.auth.models import User
from django.db.models import ExpressionWrapper, F
from django.db.models.expressions import RawSQL
from django.db.models.lookups import HasKeyLookup

class TestHasKeyLookup:

    def test_as_sqlite(self):
        # Setup
        user = User.objects.create(username='testuser', email='test@example.com', password='password')
        user_profile = {'key1': 'value1', 'key2': 'value2'}
        user.profile = json.dumps(user_profile)
        user.save()

        # Create an instance of the HasKeyLookup
        lookup = HasKeyLookup()

        # Execute as_sqlite
        sql, params = lookup.as_sqlite(None, connections['default'])

        expected_sql = 'JSON_TYPE(%s, %s) IS NOT NULL'
        assert sql == expected_sql

        # Test HasKeyLookup with a queryset
        assert User.objects.filter(profile__key1='value1').exists()
        assert not User.objects.filter(profile__key3='value3').exists()

    def test_as_sqlite_with_invalid_key(self):
        user = User.objects.create(username='testuser', email='test@example.com', password='password')
        user_profile = {'key1': 'value1'}
        user.profile = json.dumps(user_profile)
        user.save()

        lookup = HasKeyLookup()
        sql, params = lookup.as_sqlite(None, connections['default'])

        assert sql == 'JSON_TYPE(%s, %s) IS NOT NULL'
        
        # Check existence of valid key and invalid key
        assert User.objects.filter(profile__key1='value1').exists()
        assert not User.objects.filter(profile__key2='value2').exists()