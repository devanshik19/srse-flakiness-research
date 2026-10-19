import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.backends.sqlite3.base import DatabaseWrapper

@pytest.fixture
def db_wrapper():
    return DatabaseWrapper()

def test_check_constraints_no_constraints(db_wrapper):
    # Creating a user and saving it to the database
    user = User(username='testuser')
    user.save()

    # No constraints should throw no errors
    db_wrapper.check_constraints()

def test_check_constraints_with_invalid_foreign_key(db_wrapper):
    # Create a user with a foreign key constraint
    user1 = User(username='valid_user')
    user1.save()

    # Manually create a row with an invalid foreign key
    db_wrapper.cursor().execute('CREATE TABLE test_table (id INTEGER PRIMARY KEY, user_id INTEGER)')
    db_wrapper.cursor().execute('INSERT INTO test_table (id, user_id) VALUES (1, 999)')  # Invalid foreign key

    with pytest.raises(IntegrityError) as excinfo:
        db_wrapper.check_constraints(['test_table'])
    
    assert "has an invalid foreign key" in str(excinfo.value)

def test_check_constraints_supports_pragma(db_wrapper):
    db_wrapper.features.supports_pragma_foreign_key_check = True

    user1 = User(username='testuser1')
    user1.save()

    db_wrapper.cursor().execute('CREATE TABLE test_table (id INTEGER PRIMARY KEY, user_id INTEGER)')
    db_wrapper.cursor().execute('INSERT INTO test_table (id, user_id) VALUES (1, 1)')  # Valid FK

    # Check constraints should pass without errors
    db_wrapper.check_constraints(['test_table'])

    # Now insert invalid foreign key
    db_wrapper.cursor().execute('INSERT INTO test_table (id, user_id) VALUES (2, 999)')  # Invalid FK

    with pytest.raises(IntegrityError) as excinfo:
        db_wrapper.check_constraints(['test_table'])

    assert "has an invalid foreign key" in str(excinfo.value)