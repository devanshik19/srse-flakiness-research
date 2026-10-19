import base64
import pickle
from datetime import datetime
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT, BaseCache
from django.db import DatabaseError, connections, models, router, transaction
from django.utils import timezone
import pytest
from django.contrib.auth.models import User

class TestDatabaseCache:

    @pytest.fixture
    def setup_cache(self, db, cursor):
        self.cache = DatabaseCache()
        self.cache._cull_frequency = 1
        self.cache._max_entries = 5
        self.cache._table = 'django_cache'  # example table name
        self.cache.clear()  # ensure we start clean
        self.now = timezone.now()

        for i in range(10):
            self.cache.set(f'key_{i}', f'value_{i}', timeout=None)

        yield cursor

    def test_cull(self, setup_cache):
        cursor = setup_cache
        self.cache._cull('default', cursor, self.now)

        cursor.execute("SELECT COUNT(*) FROM django_cache")
        num_entries = cursor.fetchone()[0]
        
        # Check that the number of entries is less than or equal to max_entries
        assert num_entries <= self.cache._max_entries

    def test_cull_frequency_zero(self, db, cursor):
        self.cache = DatabaseCache()
        self.cache._cull_frequency = 0
        self.cache.clear()  # ensure we start clean

        # Manually add entries to the cache
        for i in range(10):
            self.cache.set(f'key_{i}', f'value_{i}', timeout=None)

        self.cache._cull('default', cursor, timezone.now())

        cursor.execute("SELECT COUNT(*) FROM django_cache")
        num_entries = cursor.fetchone()[0]

        # Ensure the cache is cleared when cull frequency is zero
        assert num_entries == 0