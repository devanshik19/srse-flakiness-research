import pytest
from django.contrib.auth.models import User
from django.db.backends.ddl_references import Table

def test_table_initialization():
    table_name = 'user_table'
    quote_name = True
    
    table = Table(table_name, quote_name)
    
    assert table.table == table_name
    assert table.quote_name is True

    # Test string representation
    assert str(table) == f"Table({table_name}, {quote_name})"

def test_table_initialization_with_different_values():
    table_name = 'admin_table'
    quote_name = False
    
    table = Table(table_name, quote_name)
    
    assert table.table == table_name
    assert table.quote_name is False

    # Test string representation
    assert str(table) == f"Table({table_name}, {quote_name})"