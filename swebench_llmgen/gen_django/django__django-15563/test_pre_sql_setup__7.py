import pytest
from django.contrib.auth.models import User
from django.db.models.sql.compiler import SQLCompiler

@pytest.fixture
def sql_compiler():
    query = User.objects.all().query
    connection = query.get_db_connection()
    return SQLCompiler(query, connection)

def test_pre_sql_setup(sql_compiler):
    # Set initial necessary attributes
    sql_compiler.select = ['id', 'username']
    sql_compiler.ordering_parts = []
    
    # Call the method under test
    extra_select, order_by, group_by = sql_compiler.pre_sql_setup()
    
    # Assert extra_select
    assert isinstance(extra_select, list)

    # Assert order_by
    assert isinstance(order_by, list)

    # Assert group_by
    assert isinstance(group_by, list)

    # Assert boolean has_extra_select indicates if there are any extra columns
    assert sql_compiler.has_extra_select is False  # Initially there should be no extra select