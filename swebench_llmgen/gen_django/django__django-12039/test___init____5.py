import pytest
from django.contrib.auth.models import User
from django.db.backends.ddl_references import Table

def test_table_init():
    table_name = 'auth_user'
    quoted_name = 'auth_user'
    
    table_instance = Table(table_name, quoted_name)
    
    assert table_instance.table == table_name
    assert table_instance.quote_name == quoted_name