import base64
import pickle
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT, BaseCache
from django.db import DatabaseError, connections, models, router, transaction
from django.utils import timezone
from django.contrib.auth.models import User
import pytest

@pytest.fixture
def database_cache():
    cache = DatabaseCache()
    cache._table = 'my_cache_table'
    cache._cull_frequency = 2
    cache._max_entries = 5
    return cache

@pytest.fixture
def setup_cache(database_cache):
    db = 'default'
    cursor = connections[db].cursor()
    now = timezone.now()
    
    cursor.execute(f"CREATE TABLE {database_cache._table} (cache_key VARCHAR(255), expires DATETIME)")
    
    # Insert 6 entries with expiration times
    for i in range(6):
        expires = now + timedelta(seconds=i)
        cursor.execute(
            f"INSERT INTO {database_cache._table} (cache_key, expires) VALUES (%s, %s)",
            [f'key_{i}', expires]
        )
    
    yield cursor, db, now

    # Clean up
    cursor.execute(f"DROP TABLE {database_cache._table}")

def test_cull_clear_cache(setup_cache, database_cache):
    cursor, db, now = setup_cache

    database_cache._cull(db, cursor, now)

    cursor.execute(f"SELECT COUNT(*) FROM {database_cache._table}")
    count = cursor.fetchone()[0]
    assert count == 5  # 6 original entries, cull frequency is 2, so 1 should be culled

def test_cull_empty_cache(database_cache):
    db = 'default'
    cursor = connections[db].cursor()
    now = timezone.now()
    
    cursor.execute(f"CREATE TABLE {database_cache._table} (cache_key VARCHAR(255), expires DATETIME)")
    cursor.execute(f"DELETE FROM {database_cache._table}")  # Ensure it's empty

    database_cache._cull(db, cursor, now)

    cursor.execute(f"SELECT COUNT(*) FROM {database_cache._table}")
    count = cursor.fetchone()[0]
    assert count == 0  # No entries should be present

def test_cull_no_cull(database_cache):
    database_cache._cull_frequency = 0  # Set to not cull

    db = 'default'
    cursor = connections[db].cursor()
    now = timezone.now()
    
    cursor.execute(f"CREATE TABLE {database_cache._table} (cache_key VARCHAR(255), expires DATETIME)")
    for i in range(3):
        expires = now + timedelta(seconds=i)
        cursor.execute(
            f"INSERT INTO {database_cache._table} (cache_key, expires) VALUES (%s, %s)",
            [f'key_{i}', expires]
        )

    database_cache._cull(db, cursor, now)

    cursor.execute(f"SELECT COUNT(*) FROM {database_cache._table}")
    count = cursor.fetchone()[0]
    assert count == 3  # No entries should be culled