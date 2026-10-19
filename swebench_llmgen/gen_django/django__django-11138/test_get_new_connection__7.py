import pytest
from django.db.backends.sqlite3.base import DatabaseWrapper
from django.db import connections

def test_get_new_connection():
    # Arrange
    db_wrapper = DatabaseWrapper()
    conn_params = {
        'database': ':memory:',
        'timeout': 5,
        'detect_types': 0,
        'isolation_level': None,
        'check_same_thread': False,
        'uri': False,
    }

    # Act
    connection = db_wrapper.get_new_connection(conn_params)

    # Assert
    assert connection is not None
    assert connection.in_transaction is False
    assert connection.execute("SELECT sqlite_version();").fetchone() is not None

    # Check custom functions are registered
    cursor = connection.cursor()
    cursor.execute("SELECT django_timestamp_diff('2021-01-01', '2021-01-02');")
    assert cursor.fetchone() is not None

    # Clean up
    connection.close()