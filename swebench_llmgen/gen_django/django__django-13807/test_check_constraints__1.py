import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.backends.sqlite3.base import DatabaseWrapper

@pytest.fixture
def db_wrapper():
    return DatabaseWrapper()

def test_check_constraints_no_violations(db_wrapper):
    # Setup: Create a user with valid foreign key references
    user = User.objects.create(username='valid_user', password='password123')
    
    # Check constraints should not raise an error with no violations
    try:
        db_wrapper.check_constraints()
    except IntegrityError:
        pytest.fail("check_constraints raised IntegrityError unexpectedly.")

def test_check_constraints_with_violations(db_wrapper):
    # Setup: Create a user and create invalid foreign key
    user = User.objects.create(username='user_with_invalid_fk', password='password123')

    # Directly manipulating database for test case - intentionally create a violation
    db_wrapper.disable_constraint_checking()
    db_wrapper.cursor().execute('INSERT INTO auth_user(id, username, password) VALUES(?, ?, ?)', (1, 'invalid_user', 'password123'))
    db_wrapper.enable_constraint_checking()

    with pytest.raises(IntegrityError) as exc_info:
        db_wrapper.check_constraints()

    assert "has an invalid foreign key" in str(exc_info.value)

def test_check_constraints_specific_tables(db_wrapper):
    # Setup: Create two users and create foreign key violations
    user1 = User.objects.create(username='user1', password='password123')
    user2 = User.objects.create(username='user2', password='password123')
    
    # Create a violation for table-specific check
    db_wrapper.disable_constraint_checking()
    db_wrapper.cursor().execute('INSERT INTO auth_user(id, username, password) VALUES(?, ?, ?)', (3, 'user_with_fk', 'password123'))  
    db_wrapper.enable_constraint_checking()

    with pytest.raises(IntegrityError) as exc_info:
        db_wrapper.check_constraints(table_names=['auth_user'])

    assert "has an invalid foreign key" in str(exc_info.value)

def test_check_constraints_empty_table_names(db_wrapper):
    # Setup: Create a valid user
    user = User.objects.create(username='no_violations', password='password123')

    # Running check_constraints with empty table_names should not raise an error
    try:
        db_wrapper.check_constraints(table_names=[])
    except IntegrityError:
        pytest.fail("check_constraints raised IntegrityError unexpectedly on empty table_names.")