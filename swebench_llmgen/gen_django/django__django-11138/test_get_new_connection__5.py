import pytest
import sqlite3
from django.db.backends.sqlite3.base import DatabaseWrapper

def test_get_new_connection():
    db_wrapper = DatabaseWrapper()

    # Simulate connection parameters for a SQLite database
    conn_params = {
        'database': ':memory:',  # Use an in-memory database for testing
    }

    # Establish a new connection
    conn = db_wrapper.get_new_connection(conn_params)

    # Verify that the connection is established
    assert isinstance(conn, sqlite3.Connection)

    # Verify that the custom functions are registered
    cursor = conn.cursor()
    
    # Test the MD5 function
    cursor.execute("SELECT MD5('test')")
    md5_result = cursor.fetchone()[0]
    assert md5_result == 'd41d8cd98f00b204e9800998ecf8427e'

    # Test the custom mathematical function (for example, ACOS)
    cursor.execute("SELECT ACOS(1)")
    acos_result = cursor.fetchone()[0]
    assert acos_result == 0.0

    # Test the standard deviation aggregate function
    cursor.execute("CREATE TABLE test_values (value REAL)")
    cursor.execute("INSERT INTO test_values (value) VALUES (1), (2), (3), (4)")
    cursor.execute("SELECT STDDEV_SAMP(value) FROM test_values")
    stddev_result = cursor.fetchone()[0]
    assert stddev_result == pytest.approx(1.2909944487358056, rel=1e-9)

    # Close the connection
    conn.close()