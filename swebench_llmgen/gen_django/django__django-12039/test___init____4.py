import pytest
from django.contrib.auth.models import User
from django.db.backends.ddl_references import Table

def test_table_init():
    # Arrange
    table_name = 'auth_user'
    quote_name = True
    
    # Act
    table_instance = Table(table_name, quote_name)

    # Assert
    assert table_instance.table == table_name
    assert table_instance.quote_name is True

def test_table_init_with_false_quote_name():
    # Arrange
    table_name = 'auth_user'
    quote_name = False
    
    # Act
    table_instance = Table(table_name, quote_name)

    # Assert
    assert table_instance.table == table_name
    assert table_instance.quote_name is False