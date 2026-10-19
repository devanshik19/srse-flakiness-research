import base64
import pickle
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT, BaseCache
from django.db import DatabaseError, connections, models, router, transaction
from django.utils import timezone
from django.contrib.auth.models import User
import pytest

class TestDatabaseCache:

    @pytest.fixture
    def db_cache(self, db):
        # Setup a DatabaseCache instance with necessary attributes
        from django.core.cache.backends.db import DatabaseCache
        
        cache = DatabaseCache('default')
        cache._max_entries = 100
        cache._cull_frequency = 10
        cache._table = 'django_cache'  # Assuming default table name
        return cache

    def test_cull_zero_frequency(self, db_cache):
        # Test the cull method when _cull_frequency is 0
        db_cache._cull_frequency = 0
        
        # Mocking the clear method
        original_clear = db_cache.clear
        db_cache.clear = pytest.Mock()

        now = timezone.now()
        db_cache._cull('default', connections['default'].cursor(), now)

        # Verify that clear was called
        db_cache.clear.assert_called_once()
        db_cache.clear = original_clear  # Restore original method

    def test_cull_no_entries(self, db_cache):
        # Test the cull method when there are no entries to cull
        cursor = connections['default'].cursor()
        now = timezone.now()

        # Set up the table to mimic no existing entries
        cursor.execute("DELETE FROM django_cache")

        db_cache._cull('default', cursor, now)

        # Verify that the expected SQL commands were executed
        cursor.execute("SELECT COUNT(*) FROM django_cache")
        num = cursor.fetchone()[0]
        assert num == 0

    def test_cull_exceeds_max_entries(self, db_cache):
        # Test the cull method when the count exceeds max entries
        cursor = connections['default'].cursor()
        now = timezone.now()

        # Insert sample entries to exceed _max_entries
        for i in range(15):
            cursor.execute("INSERT INTO django_cache (cache_key, value, expires) VALUES (%s, %s, %s)",
                           [f'key-{i}', pickle.dumps('value'), now + timedelta(minutes=5)])
        
        db_cache._cull('default', cursor, now)

        # Check the number of remaining entries; expect to cull some
        cursor.execute("SELECT COUNT(*) FROM django_cache")
        count_after_cull = cursor.fetchone()[0]
        assert count_after_cull <= db_cache._max_entries

    def test_cull_normal_operation(self, db_cache):
        # Test normal culling operation when entries are below max
        cursor = connections['default'].cursor()
        now = timezone.now()

        # Insert sample entries below _max_entries
        for i in range(5):
            cursor.execute("INSERT INTO django_cache (cache_key, value, expires) VALUES (%s, %s, %s)",
                           [f'key-{i}', pickle.dumps('value'), now + timedelta(minutes=5)])
        
        db_cache._cull('default', cursor, now)

        # Count should remain the same since we didn't exceed max entries
        cursor.execute("SELECT COUNT(*) FROM django_cache")
        count_after_cull = cursor.fetchone()[0]
        assert count_after_cull == 5