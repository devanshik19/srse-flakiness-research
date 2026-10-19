import pytest
from django.contrib.auth.models import User
from django.db import connection, transaction
from django.db.backends.sqlite3.schema import DatabaseSchemaEditor

@pytest.fixture
def database_schema_editor():
    return DatabaseSchemaEditor(connection)

def test_delete_model_handle_autom2m(database_schema_editor):
    user = User.objects.create(username='testuser')
    assert User.objects.filter(username='testuser').exists()
    
    # Calling delete_model with handle_autom2m=True
    database_schema_editor.delete_model(User, handle_autom2m=True)
    assert not User.objects.filter(username='testuser').exists()

def test_delete_model_no_handle_autom2m(database_schema_editor):
    user = User.objects.create(username='testuser')
    assert User.objects.filter(username='testuser').exists()
    
    # Calling delete_model with handle_autom2m=False
    database_schema_editor.delete_model(User, handle_autom2m=False)
    assert not User.objects.filter(username='testuser').exists()

def test_delete_model_deferred_sql_cleanup(database_schema_editor):
    user = User.objects.create(username='testuser')
    assert User.objects.filter(username='testuser').exists()
    
    # Add a deferred statement
    deferred_statement = Statement('CREATE TABLE test_deferred (id INTEGER PRIMARY KEY AUTOINCREMENT)')
    database_schema_editor.deferred_sql.append(deferred_statement)
    
    # Calling delete_model with handle_autom2m=False
    database_schema_editor.delete_model(User, handle_autom2m=False)
    
    # Check if deferred_sql is cleaned up
    assert deferred_statement not in database_schema_editor.deferred_sql