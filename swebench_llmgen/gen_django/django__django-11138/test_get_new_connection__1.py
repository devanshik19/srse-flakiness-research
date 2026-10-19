import pytest
import sqlite3
from django.db.backends.sqlite3.base import DatabaseWrapper

def test_get_new_connection():
    db_wrapper = DatabaseWrapper()

    # Define connection parameters
    conn_params = {
        'database': ':memory:',  # Use in-memory database for testing
        'timeout': 5,
        'detect_types': sqlite3.PARSE_DECLTYPES,
    }

    # Invoke the focal function
    connection = db_wrapper.get_new_connection(conn_params)

    # Check that the connection is successful and valid
    assert connection is not None
    assert isinstance(connection, sqlite3.Connection)

    # Test that custom functions are registered correctly
    cursor = connection.cursor()
    cursor.execute("SELECT django_date_extract('now', 'year')")
    year = cursor.fetchone()[0]
    
    assert isinstance(year, int)  # Assuming the year will be an integer
    assert year == datetime.datetime.now().year  # Check it matches the current year

    cursor.execute("SELECT ACOS(1)")  # Test a math function
    acos_result = cursor.fetchone()[0]
    assert acos_result == 0.0  # ACOS(1) should return 0

    cursor.execute("SELECT SHA256('test')")  # Test a built-in function
    sha256_result = cursor.fetchone()[0]
    expected_sha256 = hashlib.sha256(b'test').hexdigest()
    
    assert sha256_result == expected_sha256

    # Clean up
    cursor.close()
    connection.close()