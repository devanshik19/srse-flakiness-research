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

    @pytest.fixture(autouse=True)
    def setup_method(self, db):
        self.cache = DatabaseCache()
        self.cache._table = 'test_cache'
        self.cache._max_entries = 5
        self.cache._cull_frequency = 2
        
        # Create the cache table
        with connections['default'].cursor() as cursor:
            cursor.execute("""
                CREATE TABLE test_cache (
                    cache_key VARCHAR(255) NOT NULL PRIMARY KEY,
                    expires DATETIME NOT NULL
                )
            """)
    
    def test_cull_no_entries(self):
        now = timezone.now()
        with connections['default'].cursor() as cursor:
            self.cache._cull('default', cursor, now)
            cursor.execute("SELECT COUNT(*) FROM %s" % self.cache._table)
            num = cursor.fetchone()[0]
            assert num == 0

    def test_cull_with_entries(self):
        now = timezone.now()
        future_time = now + timezone.timedelta(days=1)
        past_time = now - timezone.timedelta(days=1)

        with connections['default'].cursor() as cursor:
            cursor.execute("INSERT INTO %s (cache_key, expires) VALUES (%s, %s)" % (self.cache._table, '%s', '%s'), ['key1', future_time])
            cursor.execute("INSERT INTO %s (cache_key, expires) VALUES (%s, %s)" % (self.cache._table, '%s', '%s'), ['key2', past_time])
            cursor.execute("INSERT INTO %s (cache_key, expires) VALUES (%s, %s)" % (self.cache._table, '%s', '%s'), ['key3', future_time])
            cursor.execute("INSERT INTO %s (cache_key, expires) VALUES (%s, %s)" % (self.cache._table, '%s', '%s'), ['key4', past_time])
            cursor.execute("INSERT INTO %s (cache_key, expires) VALUES (%s, %s)" % (self.cache._table, '%s', '%s'), ['key5', future_time])
            cursor.execute("INSERT INTO %s (cache_key, expires) VALUES (%s, %s)" % (self.cache._table, '%s', '%s'), ['key6', past_time])

            self.cache._cull('default', cursor, now)

            cursor.execute("SELECT COUNT(*) FROM %s" % self.cache._table)
            num_remaining = cursor.fetchone()[0]
            assert num_remaining == 3
            
            cursor.execute("SELECT cache_key FROM %s" % self.cache._table)
            remaining_keys = [row[0] for row in cursor.fetchall()]
            assert set(remaining_keys) == {'key1', 'key3', 'key5'}

    def test_cull_frequency_zero(self):
        self.cache._cull_frequency = 0
        now = timezone.now()
        with connections['default'].cursor() as cursor:
            cursor.execute("INSERT INTO %s (cache_key, expires) VALUES (%s, %s)" % (self.cache._table, '%s', '%s'), ['key1', now])
            self.cache._cull('default', cursor, now)

            cursor.execute("SELECT COUNT(*) FROM %s" % self.cache._table)
            num = cursor.fetchone()[0]
            assert num == 0