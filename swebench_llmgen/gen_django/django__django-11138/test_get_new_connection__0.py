import pytest
import sqlite3
from django.db.backends.sqlite3.base import DatabaseWrapper

def test_get_new_connection():
    db_wrapper = DatabaseWrapper()
    
    # Define connection parameters
    conn_params = {
        'database': ':memory:',  # Use in-memory database for testing
        'timeout': 5,
        'detect_types': sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    }

    # Verify that a new connection is established
    conn = db_wrapper.get_new_connection(conn_params)
    
    # Check if the connection is a sqlite3.Connection instance
    assert isinstance(conn, sqlite3.Connection)

    # Check if the custom SQLite functions are correctly registered
    functions = conn.execute("SELECT name FROM sqlite_master WHERE type='function';").fetchall()
    function_names = {function[0] for function in functions}
    
    # List all the expected function names
    expected_functions = [
        "django_date_extract", "django_date_trunc", "django_datetime_cast_date",
        "django_datetime_cast_time", "django_datetime_extract", "django_datetime_trunc",
        "django_time_extract", "django_time_trunc", "django_time_diff",
        "django_timestamp_diff", "django_format_dtdelta", "regexp", "ACOS", 
        "ASIN", "ATAN", "ATAN2", "CEILING", "COS", "COT", "DEGREES", "EXP", 
        "FLOOR", "LN", "LOG", "LPAD", "MD5", "MOD", "PI", "POWER", "RADIANS", 
        "REPEAT", "REVERSE", "RPAD", "SHA1", "SHA224", "SHA256", "SHA384", 
        "SHA512", "SIGN", "SIN", "SQRT", "TAN", "STDDEV_POP", "STDDEV_SAMP", 
        "VAR_POP", "VAR_SAMP"
    ]
    
    # Check if all expected functions are registered
    for func in expected_functions:
        assert func in function_names

    # Check if foreign key constraints are enabled
    pragma_foreign_keys = conn.execute("PRAGMA foreign_keys;").fetchone()
    assert pragma_foreign_keys[0] == 1  # Should return 1 if foreign keys are enabled

    # Clean up
    conn.close()