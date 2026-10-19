import pytest
import sqlite3
from django.db.backends.sqlite3.base import DatabaseWrapper

def test_get_new_connection():
    db_wrapper = DatabaseWrapper()

    # Prepare connection parameters
    conn_params = {
        'database': ':memory:',
        'timeout': 5,
        'detect_types': sqlite3.PARSE_DECLTYPES,
    }

    # Create a new connection
    conn = db_wrapper.get_new_connection(conn_params)

    # Check if connection is successfully established
    assert conn is not None

    # Confirm that SQLite functions have been registered
    cursor = conn.cursor()

    # Test some of the custom functions
    cursor.execute("SELECT django_date_extract('year', '2023-01-01')")
    year_extracted = cursor.fetchone()[0]
    assert year_extracted == 2023

    cursor.execute("SELECT django_time_diff('2023-01-01 12:00:00', '2023-01-01 10:00:00')")
    time_diff = cursor.fetchone()[0]
    assert time_diff is not None  # diff should not be None

    cursor.execute("SELECT MD5('test')")
    md5_hash = cursor.fetchone()[0]
    assert md5_hash == '5f4dcc3b5aa765d61d8327deb882cf99'  # Hash of 'test'

    # Cleanup
    cursor.close()
    conn.close()