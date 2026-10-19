import base64
import pickle
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache.backends.db import DatabaseCache
from django.db import connections
from django.contrib.auth.models import User
import pytest

@pytest.fixture
def db_cache():
    db_cache = DatabaseCache()
    db_cache._table = 'test_cache_table'
    db_cache._cull_frequency = 2
    db_cache._max_entries = 5
    return db_cache

@pytest.fixture
def populate_cache(db_cache, db, cursor):
    now = timezone.now()
    # Insert cache entries
    for i in range(10):
        cursor.execute(
            f"INSERT INTO {db_cache._table} (cache_key, value, expires) VALUES (%s, %s, %s)",
            [f"key_{i}", pickle.dumps(User(username=f'user_{i}')), now + timedelta(minutes=5)]
        )

def test_cull_no_frequency(db_cache, db, cursor):
    db_cache._cull_frequency = 0  # No culling
    db_cache.clear = lambda: None  # Mock clear to avoid executing it
    now = timezone.now()
    
    db_cache._cull('default', cursor, now)
    
    cursor.execute(f"SELECT COUNT(*) FROM {db_cache._table}")
    num_entries = cursor.fetchone()[0]
    
    assert num_entries == 10  # All entries should remain

def test_cull_with_frequency(db_cache, populate_cache, db, cursor):
    now = timezone.now()
    
    db_cache._cull('default', cursor, now)
    
    cursor.execute(f"SELECT COUNT(*) FROM {db_cache._table}")
    num_entries_after_cull = cursor.fetchone()[0]
    
    assert num_entries_after_cull <= 5  # Should have removed some entries

def test_cull_removes_based_on_threshold(db_cache, populate_cache, db, cursor):
    now = timezone.now() + timedelta(minutes=10)  # Simulate future time
    db_cache._cull('default', cursor, now)
    
    cursor.execute(f"SELECT COUNT(*) FROM {db_cache._table}")
    num_entries_after_cull = cursor.fetchone()[0]
    
    assert num_entries_after_cull == 10  # Should not remove anything if `now` is in the future