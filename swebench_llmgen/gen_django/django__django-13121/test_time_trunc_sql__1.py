import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.mysql.operations import DatabaseOperations

def test_time_trunc_sql():
    # Create an instance of DatabaseOperations
    ops = DatabaseOperations()

    # Define test cases
    test_cases = [
        ('hour', 'created_at', "CAST(DATE_FORMAT(created_at, '%H:00:00') AS TIME)"),
        ('minute', 'created_at', "CAST(DATE_FORMAT(created_at, '%H:%i:00') AS TIME)"),
        ('second', 'created_at', "CAST(DATE_FORMAT(created_at, '%H:%i:%s') AS TIME)"),
        ('unknown', 'created_at', "TIME(created_at)")
    ]

    for lookup_type, field_name, expected_sql in test_cases:
        sql = ops.time_trunc_sql(lookup_type, field_name)
        assert sql == expected_sql

    # Test with actual User instances
    user = User.objects.create(username='test_user', email='user@test.com', password='testpass')

    # Verify the created user can be queried
    sql = ops.time_trunc_sql('hour', 'user.created_at')
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT {sql} FROM auth_user WHERE id = %s", [user.id])
        result = cursor.fetchone()
        assert result is not None