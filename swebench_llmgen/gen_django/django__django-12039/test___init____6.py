import pytest
from django.contrib.auth.models import User
from django.db.backends.ddl_references import Table

def test_table_init():
    # Create a sample user to represent the table data
    user = User.objects.create(username='testuser')
    table_name = user._meta.db_table
    quoted_name = f'"{table_name}"'

    # Initialize the Table instance
    table_instance = Table(table=table_name, quote_name=quoted_name)

    # Check that the properties are set correctly
    assert table_instance.table == table_name
    assert table_instance.quote_name == quoted_name

    # Test the string representation
    assert str(table_instance) == quoted_name