import pytest
from django.contrib.auth.models import User
from django.db.backends.sqlite3.base import DatabaseWrapper

def test_get_new_connection():
    # Setup
    db_wrapper = DatabaseWrapper()
    conn_params = db_wrapper.get_connection_params()
    
    # Act
    connection = db_wrapper.get_new_connection(conn_params)

    # Verify connection is established
    assert connection is not None
    assert connection.in_transaction is False  # Ensure no transaction is active
    
    # Confirm that the custom functions exist
    functions_to_check = [
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
    
    # Check that all custom functions were registered
    for function in functions_to_check:
        result = connection.execute(f"SELECT {function}(1)").fetchone()
        assert result is not None  # Ensure the function returns a result or doesn't throw an error

    # Cleanup
    connection.close()