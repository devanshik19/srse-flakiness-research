import pytest
from django.contrib.auth.models import User
from django.db.backends.ddl_references import Table

def test_table_init():
    table_name = 'auth_user'
    quote_name = True

    table_instance = Table(table_name, quote_name)
    
    assert table_instance.table == table_name
    assert table_instance.quote_name == quote_name

    # Testing with different input values
    table_name_2 = 'auth_group'
    quote_name_2 = False

    table_instance_2 = Table(table_name_2, quote_name_2)
    
    assert table_instance_2.table == table_name_2
    assert table_instance_2.quote_name == quote_name_2