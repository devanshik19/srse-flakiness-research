import pytest
from django.contrib.auth.models import User
from django.db.backends.ddl_references import Table

def test_table_init():
    table_name = 'auth_user'
    quote_name = True
    table_instance = Table(table=table_name, quote_name=quote_name)

    assert table_instance.table == table_name
    assert table_instance.quote_name == quote_name

    table_instance_2 = Table(table='custom_table', quote_name=False)
    assert table_instance_2.table == 'custom_table'
    assert table_instance_2.quote_name is False