import pytest
from django.contrib.auth.models import User
from django.db.backends.ddl_references import Table

def test_table_initialization():
    table_name = 'auth_user'
    quote_name = '"auth_user"'

    # Initialize the Table instance
    table = Table(table=table_name, quote_name=quote_name)

    # Assert the internal state
    assert table.table == table_name
    assert table.quote_name == quote_name