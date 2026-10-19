import pytest
from django.contrib.auth.models import User
from django.db.backends.sqlite3.base import DatabaseWrapper

def test_get_new_connection():
    db_wrapper = DatabaseWrapper()
    conn_params = {
        'database': 'test_db.sqlite3',
        'timeout': 5.0,
        'detect_types': 0,
        'check_same_thread': False
    }
    
    # Attempt to create a new connection
    connection = db_wrapper.get_new_connection(conn_params)

    # Validate that the connection is established and not None
    assert connection is not None

    # Validate that we can use the connection to create a cursor
    cursor = connection.cursor()
    assert cursor is not None

    # Clean up cursor and connection
    cursor.close()
    connection.close()

    # Validate custom SQLite functions
    try:
        connection = db_wrapper.get_new_connection(conn_params)
        cursor = connection.cursor()

        # Test a custom SQLite function if applicable
        cursor.execute("SELECT django_date_extract('2022-01-01', 'year')")
        result = cursor.fetchone()
        assert result is not None

    finally:
        cursor.close()
        connection.close()