import pytest
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.db.backends.sqlite3.base import DatabaseWrapper

@pytest.mark.django_db
def test_check_constraints_with_invalid_foreign_key():
    # Setup: Create two users, one with a valid foreign key relation and another with an invalid one.
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    # Directly create an invalid foreign key reference in SQLite
    db_wrapper = DatabaseWrapper()
    db_wrapper.disable_constraint_checking()  # Disable checks temporarily
    db_wrapper.cursor().execute("CREATE TABLE example_table (id INTEGER PRIMARY KEY, user_id INTEGER);")
    db_wrapper.cursor().execute("INSERT INTO example_table (user_id) VALUES (?)", (user1.id,))
    db_wrapper.cursor().execute("INSERT INTO example_table (user_id) VALUES (9999);")  # Invalid user_id
    db_wrapper.enable_constraint_checking()  # Re-enable checks

    # Act: Check constraints should raise an IntegrityError due to invalid user_id reference
    with pytest.raises(IntegrityError) as excinfo:
        db_wrapper.check_constraints(['example_table'])

    # Assert: Check that the message contains expected text related to the invalid foreign key
    assert "has an invalid foreign key" in str(excinfo.value)

@pytest.mark.django_db
def test_check_constraints_no_invalid_foreign_key():
    # Setup: Create only valid foreign key relations
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    # Create a table with valid foreign key reference
    db_wrapper = DatabaseWrapper()
    db_wrapper.disable_constraint_checking()
    db_wrapper.cursor().execute("CREATE TABLE example_table (id INTEGER PRIMARY KEY, user_id INTEGER);")
    db_wrapper.cursor().execute("INSERT INTO example_table (user_id) VALUES (?)", (user1.id,))
    db_wrapper.enable_constraint_checking() 

    # Act: Check constraints should not raise an IntegrityError
    try:
        db_wrapper.check_constraints(['example_table'])  # No exception should occur
    except IntegrityError:
        pytest.fail("check_constraints raised IntegrityError unexpectedly.")

@pytest.mark.django_db
def test_check_constraints_multiple_tables():
    # Setup: Create users and multiple tables with valid and invalid foreign key references
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    db_wrapper = DatabaseWrapper()
    db_wrapper.disable_constraint_checking()
    
    db_wrapper.cursor().execute("CREATE TABLE valid_table (id INTEGER PRIMARY KEY, user_id INTEGER);")
    db_wrapper.cursor().execute("CREATE TABLE invalid_table (id INTEGER PRIMARY KEY, user_id INTEGER);")
    
    db_wrapper.cursor().execute("INSERT INTO valid_table (user_id) VALUES (?)", (user1.id,))
    db_wrapper.cursor().execute("INSERT INTO invalid_table (user_id) VALUES (9999);")  # Invalid user_id

    db_wrapper.enable_constraint_checking()

    # Act: Check constraints on both tables should raise an IntegrityError for the invalid one
    with pytest.raises(IntegrityError) as excinfo:
        db_wrapper.check_constraints(['valid_table', 'invalid_table'])

    # Assert: Check that the message contains expected text related to the invalid foreign key
    assert "has an invalid foreign key" in str(excinfo.value)