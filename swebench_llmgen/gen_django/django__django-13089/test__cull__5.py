import pytest
from django.contrib.auth.models import User
from django.db import connections, transaction
from django.core.cache.backends.db import DatabaseCache
from datetime import datetime, timedelta

@pytest.fixture
def db_cache():
    return DatabaseCache()

def test_cull_no_cull_frequency(db_cache):
    db_cache._cull_frequency = 0
    db_cache.clear = lambda: None
    db_cache._cull('default', connections['default'].cursor(), datetime.now())
    assert db_cache.clear.called

def test_cull_with_cull_frequency(db_cache, django_db_blocker):
    db_cache._cull_frequency = 3
    db_cache._max_entries = 5
    now = datetime.now()

    with django_db_blocker.unblock():
        user = User.objects.create(username='testuser')
        db_cache.set('key1', 'value1', timeout=DEFAULT_TIMEOUT)
        db_cache.set('key2', 'value2', timeout=DEFAULT_TIMEOUT)
        db_cache.set('key3', 'value3', timeout=DEFAULT_TIMEOUT)
        db_cache.set('key4', 'value4', timeout=DEFAULT_TIMEOUT)
        db_cache.set('key5', 'value5', timeout=DEFAULT_TIMEOUT)
        db_cache.set('key6', 'value6', timeout=DEFAULT_TIMEOUT)  # Over the max entries limit

        db_cache._cull('default', connections['default'].cursor(), now)

        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM %s" % db_cache._table)
            remaining_count = cursor.fetchone()[0]
            assert remaining_count <= db_cache._max_entries

            cursor.execute("SELECT cache_key FROM %s ORDER BY cache_key" % db_cache._table)
            cache_keys = cursor.fetchall()
            assert len(cache_keys) == remaining_count

            # Test that keys have been culled if they exceed the max entries
            assert cache_keys[0][0] == 'key1'  # Assumes keys are sorted by creation