import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.backends.sqlite3.base import DatabaseWrapper

def test_check_constraints_no_violations(db, settings):
    # Arrange
    user = User.objects.create(username='testuser', password='testpass')
    db_wrapper = DatabaseWrapper()

    # Act
    try:
        db_wrapper.check_constraints()
    except IntegrityError:
        pytest.fail("IntegrityError raised unexpectedly")

def test_check_constraints_with_violations(db, settings):
    # Arrange
    user = User.objects.create(username='testuser', password='testpass')
    db_wrapper = DatabaseWrapper()

    # Simulating a broken foreign key constraint setup
    db_wrapper.cursor().execute("CREATE TABLE parent (id INTEGER PRIMARY KEY AUTOINCREMENT)")
    db_wrapper.cursor().execute("CREATE TABLE child (id INTEGER PRIMARY KEY AUTOINCREMENT, parent_id INTEGER)")
    db_wrapper.cursor().execute("INSERT INTO child (parent_id) VALUES (1)")  # This will cause a violation
    db_wrapper.disable_constraint_checking()

    # Act
    db_wrapper.cursor().execute("INSERT INTO parent (id) VALUES (2)")  # This inserts valid reference

    # Assert
    with pytest.raises(IntegrityError) as exc_info:
        db_wrapper.check_constraints(['child'])

    assert "has an invalid foreign key" in str(exc_info.value)
    assert "child.parent_id contains a value '1'" in str(exc_info.value)

    db_wrapper.enable_constraint_checking()  # Clean up if needed