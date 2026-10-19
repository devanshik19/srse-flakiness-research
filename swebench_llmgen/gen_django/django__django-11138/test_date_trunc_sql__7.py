import pytest
from django.db.backends.sqlite3.operations import DatabaseOperations

def test_date_trunc_sql():
    operations = DatabaseOperations()

    # Test with different lookup types
    result1 = operations.date_trunc_sql('second', 'created_at')
    assert result1 == "django_date_trunc('second', created_at)"

    result2 = operations.date_trunc_sql('minute', 'updated_at')
    assert result2 == "django_date_trunc('minute', updated_at)"

    result3 = operations.date_trunc_sql('hour', 'last_login')
    assert result3 == "django_date_trunc('hour', last_login)"

    # Test with different case sensitivity
    result4 = operations.date_trunc_sql('DAY', 'birth_date')
    assert result4 == "django_date_trunc('day', birth_date)"

    result5 = operations.date_trunc_sql('WEEK', 'signup_date')
    assert result5 == "django_date_trunc('week', signup_date)"