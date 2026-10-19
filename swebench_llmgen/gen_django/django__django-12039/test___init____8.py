import pytest
from django.contrib.auth.models import User
from django.db.backends.ddl_references import Table

def test_table_init():
    # Arrange
    table_name = "auth_user"
    quote_name = "auth_user"

    # Act
    table = Table(table_name, quote_name)

    # Assert
    assert table.table == table_name
    assert table.quote_name == quote_name

def test_table_str():
    # Arrange
    table_name = "auth_user"
    quote_name = "auth_user"
    table = Table(table_name, quote_name)

    # Act
    table_str = str(table)

    # Assert
    assert table_str == f'Table(table={table_name}, quote_name={quote_name})'