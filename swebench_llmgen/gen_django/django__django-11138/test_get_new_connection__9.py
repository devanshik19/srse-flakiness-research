import pytest
from django.contrib.auth.models import User
from django.db.backends.sqlite3.base import DatabaseWrapper


def test_get_new_connection():
    # Prepare connection parameters
    conn_params = {
        'database': ':memory:',  # using in-memory database for testing
        'detect_types': Database.PARSE_DECLTYPES | Database.PARSE_COLNAMES,
    }
    
    # Create an instance of DatabaseWrapper
    db_wrapper = DatabaseWrapper()

    # Call the method under test
    connection = db_wrapper.get_new_connection(conn_params)

    # Check that the connection is established
    assert connection is not None

    # Check that we can create a table and insert data using the custom functions
    connection.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT)")
    connection.execute("INSERT INTO users (username) VALUES (?)", ('test_user',))
    
    # Check that the inserted data can be retrieved
    cursor = connection.execute("SELECT username FROM users WHERE id = 1")
    user = cursor.fetchone()
    assert user[0] == 'test_user'

    # Check if a function can be created
    cursor.execute("SELECT MD5('test')")  # Using one of the custom functions
    md5_result = cursor.fetchone()[0]
    assert md5_result == 'd41d8cd98f00b204e9800998ecf8427e'  # Check against the expected MD5 hash

    # Close the connection
    connection.close()