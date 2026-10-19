import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.backends.sqlite3.base import DatabaseWrapper

@pytest.fixture
def db_wrapper(database):
    return DatabaseWrapper()

def test_check_constraints_no_violations(db_wrapper):
    # Setup: Create a valid User instance
    User.objects.create(username='testuser', password='password123')

    # Execute: Check constraints for all tables
    try:
        db_wrapper.check_constraints()
    except IntegrityError:
        pytest.fail("IntegrityError raised unexpectedly.")

def test_check_constraints_with_violations(db_wrapper):
    # Setup: Create a valid User and manually violate foreign key constraints
    user = User.objects.create(username='testuser', password='password123')
    # Assuming some operation that creates a violation (e.g., direct SQL execution)
    db_wrapper.cursor().execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, user_id INTEGER)")
    db_wrapper.cursor().execute("INSERT INTO test_table (user_id) VALUES (999)")  # Invalid FK

    # Execute: Check constraints for specific tables
    with pytest.raises(IntegrityError) as exc_info:
        db_wrapper.check_constraints(table_names=['test_table'])
    
    # Verify: Ensure error message contains expected detail
    assert "invalid foreign key" in str(exc_info.value)

def test_check_constraints_empty_table_names(db_wrapper):
    # Setup: Create two valid Users
    User.objects.create(username='user1', password='pass1')
    User.objects.create(username='user2', password='pass2')

    # Execute: Check constraints with empty table_names
    try:
        db_wrapper.check_constraints(table_names=[])
    except IntegrityError:
        pytest.fail("IntegrityError raised unexpectedly for empty table_names.")