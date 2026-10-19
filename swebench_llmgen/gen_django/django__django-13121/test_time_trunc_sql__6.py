import uuid
from django.conf import settings
from django.db.backends.mysql.operations import DatabaseOperations
from django.contrib.auth.models import User
import pytest

@pytest.mark.parametrize("lookup_type, field_name, expected_sql", [
    ('hour', 'created_at', "CAST(DATE_FORMAT(created_at, '%H:00:00') AS TIME)"),
    ('minute', 'updated_at', "CAST(DATE_FORMAT(updated_at, '%H:%i:00') AS TIME)"),
    ('second', 'login_time', "CAST(DATE_FORMAT(login_time, '%H:%i:%s') AS TIME)"),
    ('day', 'signup_time', "TIME(signup_time)"),
])
def test_time_trunc_sql(lookup_type, field_name, expected_sql):
    # Initialize DatabaseOperations instance
    operations = DatabaseOperations()
    
    # Create a User instance to have a context for the field names
    User.objects.create(username='testuser', password='password123', email='test@example.com')

    # Calling the time_trunc_sql method
    sql = operations.time_trunc_sql(lookup_type, field_name)
    
    # Assert that the generated SQL matches the expected SQL
    assert sql == expected_sql