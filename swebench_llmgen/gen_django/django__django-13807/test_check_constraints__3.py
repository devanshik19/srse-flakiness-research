import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.backends.sqlite3.base import DatabaseWrapper

def test_check_constraints_no_violations(database):
    db_wrapper = DatabaseWrapper()

    # Create a test table and insert valid data
    with db_wrapper.cursor() as cursor:
        cursor.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES auth_user(id))")
        cursor.execute("INSERT INTO auth_user (username) VALUES ('testuser')")
        user_id = cursor.lastrowid
        cursor.execute("INSERT INTO test_table (user_id) VALUES (?)", (user_id,))

    # Invoke check_constraints without specifying tables
    try:
        db_wrapper.check_constraints()
    except IntegrityError:
        pytest.fail("check_constraints raised IntegrityError unexpectedly.")

def test_check_constraints_with_violations(database):
    db_wrapper = DatabaseWrapper()

    # Create a test table and insert invalid data
    with db_wrapper.cursor() as cursor:
        cursor.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES auth_user(id))")
        # Here we add a row with a non-existent user_id
        cursor.execute("INSERT INTO test_table (user_id) VALUES (999)")

    # Check for IntegrityError when checking constraints
    with pytest.raises(IntegrityError) as excinfo:
        db_wrapper.check_constraints()

    # Validate the error message for clarity
    expected_message = "does not have a corresponding value in auth_user.id."
    assert expected_message in str(excinfo.value)

def test_check_constraints_specific_tables(database):
    db_wrapper = DatabaseWrapper()

    # Create a test table and valid user
    with db_wrapper.cursor() as cursor:
        cursor.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES auth_user(id))")
        cursor.execute("INSERT INTO auth_user (username) VALUES ('testuser')")
        user_id = cursor.lastrowid
        cursor.execute("INSERT INTO test_table (user_id) VALUES (?)", (user_id,))

    # Create another table with an invalid FK reference
    with db_wrapper.cursor() as cursor:
        cursor.execute("CREATE TABLE another_table (id INTEGER PRIMARY KEY, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES auth_user(id))")
        cursor.execute("INSERT INTO another_table (user_id) VALUES (999)")

    # Check only the specific 'another_table' for constraint violations
    with pytest.raises(IntegrityError):
        db_wrapper.check_constraints(table_names=['another_table'])