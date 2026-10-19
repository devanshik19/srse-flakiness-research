import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.backends.sqlite3.base import DatabaseWrapper

@pytest.fixture
def db_wrapper():
    return DatabaseWrapper()

def test_check_constraints_no_violations(db_wrapper):
    # Create a table with valid foreign key references
    db_wrapper.cursor().execute('CREATE TABLE parent (id INTEGER PRIMARY KEY)')
    db_wrapper.cursor().execute('CREATE TABLE child (id INTEGER PRIMARY KEY, parent_id INTEGER, FOREIGN KEY(parent_id) REFERENCES parent(id))')
    db_wrapper.cursor().execute('INSERT INTO parent (id) VALUES (1)')
    db_wrapper.cursor().execute('INSERT INTO child (id, parent_id) VALUES (1, 1)')

    # Run check_constraints without specifying table names
    try:
        db_wrapper.check_constraints()
    except IntegrityError:
        pytest.fail("IntegrityError raised when there should be no violations.")

def test_check_constraints_with_violations(db_wrapper):
    # Create a table with a foreign key reference
    db_wrapper.cursor().execute('CREATE TABLE parent (id INTEGER PRIMARY KEY)')
    db_wrapper.cursor().execute('CREATE TABLE child (id INTEGER PRIMARY KEY, parent_id INTEGER, FOREIGN KEY(parent_id) REFERENCES parent(id))')
    db_wrapper.cursor().execute('INSERT INTO parent (id) VALUES (1)')
    db_wrapper.cursor().execute('INSERT INTO child (id, parent_id) VALUES (1, 2)')  # Invalid foreign key

    with pytest.raises(IntegrityError) as excinfo:
        db_wrapper.check_constraints()
    
    assert "The row in table 'child'" in str(excinfo.value)

def test_check_constraints_specific_tables(db_wrapper):
    # Create a table with valid references and another with an invalid reference
    db_wrapper.cursor().execute('CREATE TABLE parent (id INTEGER PRIMARY KEY)')
    db_wrapper.cursor().execute('CREATE TABLE child (id INTEGER PRIMARY KEY, parent_id INTEGER, FOREIGN KEY(parent_id) REFERENCES parent(id))')
    db_wrapper.cursor().execute('INSERT INTO parent (id) VALUES (1)')
    db_wrapper.cursor().execute('INSERT INTO child (id, parent_id) VALUES (1, 2)')  # Invalid foreign key

    with pytest.raises(IntegrityError) as excinfo:
        db_wrapper.check_constraints(table_names=['child'])
    
    assert "The row in table 'child'" in str(excinfo.value)

def test_check_constraints_no_tables(db_wrapper):
    # Create an empty table
    db_wrapper.cursor().execute('CREATE TABLE empty (id INTEGER PRIMARY KEY)')

    try:
        db_wrapper.check_constraints()  # Should not raise any exception
    except IntegrityError:
        pytest.fail("IntegrityError raised when there should be no violations on an empty table.")