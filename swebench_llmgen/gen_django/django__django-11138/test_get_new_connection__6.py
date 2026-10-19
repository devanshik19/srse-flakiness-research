import pytest
from django.db.backends.sqlite3.base import DatabaseWrapper

def test_get_new_connection_creates_functions():
    db_wrapper = DatabaseWrapper()
    conn_params = {'database': ':memory:'}  # Use in-memory database for testing
    connection = db_wrapper.get_new_connection(conn_params)
    
    # Verify that the functions have been created in the SQLite connection
    fxns = [
        "django_date_extract",
        "django_date_trunc",
        "django_datetime_cast_date",
        "django_datetime_cast_time",
        "django_datetime_extract",
        "django_datetime_trunc",
        "django_time_extract",
        "django_time_trunc",
        "django_time_diff",
        "django_timestamp_diff",
        "django_format_dtdelta",
        "regexp",
        "ACOS", "ASIN", "ATAN", "ATAN2", "CEILING", "COS", "COT",
        "DEGREES", "EXP", "FLOOR", "LN", "LOG", "LPAD", "MD5",
        "MOD", "PI", "POWER", "RADIANS", "REPEAT", "REVERSE", 
        "RPAD", "SHA1", "SHA224", "SHA256", "SHA384", "SHA512",
        "SIGN", "SIN", "SQRT", "TAN", 
        "STDDEV_POP", "STDDEV_SAMP", "VAR_POP", "VAR_SAMP"
    ]

    for func in fxns:
        with pytest.raises(Exception) as excinfo:
            connection.execute(f"SELECT {func}()")
        assert "no such function" not in str(excinfo.value)
    
    connection.close()