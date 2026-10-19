import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.backends.sqlite3.base import DatabaseWrapper

def test_check_constraints_no_violations(db):
    db_wrapper = DatabaseWrapper()
    db_wrapper.enable_constraint_checking()  # Ensure constraints are enabled

    # Create a user instance to ensure the table is created
    user = User.objects.create_user(username='testuser', password='testpass')

    # Check constraints with no violations
    try:
        db_wrapper.check_constraints()
    except IntegrityError:
        pytest.fail("check_constraints raised IntegrityError unexpectedly.")

def test_check_constraints_with_violations(db):
    db_wrapper = DatabaseWrapper()
    db_wrapper.disable_constraint_checking()  # Disable constraints temporarily

    # Create a user instance to ensure the table is created
    user = User.objects.create_user(username='testuser', password='testpass')

    # Create a malformed foreign key scenario
    with db_wrapper.cursor() as cursor:
        cursor.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, user_id INTEGER)")
        cursor.execute("INSERT INTO test_table (user_id) VALUES (999)")  # Invalid user_id

    db_wrapper.enable_constraint_checking()  # Re-enable constraints

    # Now check constraints expecting an IntegrityError
    with pytest.raises(IntegrityError) as excinfo:
        db_wrapper.check_constraints()

    assert "invalid foreign key" in str(excinfo.value)

def test_check_constraints_with_specific_table(db):
    db_wrapper = DatabaseWrapper()
    db_wrapper.disable_constraint_checking()  # Disable constraints temporarily

    # Create a user instance to ensure the table is created
    user = User.objects.create_user(username='testuser', password='testpass')

    # Create a malformed foreign key scenario
    with db_wrapper.cursor() as cursor:
        cursor.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, user_id INTEGER)")
        cursor.execute("INSERT INTO test_table (user_id) VALUES (999)")  # Invalid user_id

    db_wrapper.enable_constraint_checking()  # Re-enable constraints

    # Check constraints on a specific table expecting an IntegrityError
    with pytest.raises(IntegrityError) as excinfo:
        db_wrapper.check_constraints(table_names=['test_table'])

    assert "invalid foreign key" in str(excinfo.value)