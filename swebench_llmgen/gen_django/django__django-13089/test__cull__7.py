import pytest
from django.contrib.auth.models import User
from django.core.cache.backends.db import DatabaseCache
from django.db import connection

@pytest.mark.django_db
def test_cull():
    # Setup cache
    cache = DatabaseCache('default')
    cache._table = 'django_cache'
    cache._cull_frequency = 2
    cache._max_entries = 5
    
    # Setup cursor
    cursor = connection.cursor()
    
    # Create table for cache
    cursor.execute("""
        CREATE TABLE django_cache (
            cache_key VARCHAR(255) NOT NULL PRIMARY KEY,
            expires DATETIME NOT NULL
        )
    """)
    
    # Set current time
    now = timezone.now()

    # Insert entries into cache with varying expiration times
    cursor.execute("""
        INSERT INTO django_cache (cache_key, expires) VALUES
        ('key1', %s), ('key2', %s), ('key3', %s), ('key4', %s), ('key5', %s)
    """, [now + timezone.timedelta(seconds=10)] * 5)

    # Calling _cull to remove expired entries
    cache._cull('default', cursor, now + timezone.timedelta(seconds=15))

    # Ensure that after culling, we don't have more than 5 entries
    cursor.execute("SELECT COUNT(*) FROM django_cache")
    num_entries = cursor.fetchone()[0]
    assert num_entries == 0  # Expecting all entries to be culled

    # Add entries again
    cursor.execute("""
        INSERT INTO django_cache (cache_key, expires) VALUES
        ('key6', %s), ('key7', %s)
    """, [now + timezone.timedelta(seconds=5)] * 2)
    
    # Double the cull frequency to remove keys if entries exceed max
    cache._cull_frequency = 1

    # Call _cull which now should remove key6 based on logic
    cache._cull('default', cursor, now + timezone.timedelta(seconds=10))

    # Confirming that one record has been culled
    cursor.execute("SELECT COUNT(*) FROM django_cache")
    num_entries_after_cull = cursor.fetchone()[0]
    assert num_entries_after_cull == 1  # Expecting one entry to remain (key7)

    # Cleanup
    cursor.execute("DROP TABLE django_cache")