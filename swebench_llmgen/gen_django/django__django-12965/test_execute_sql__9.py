import pytest
from django.db import connection
from django.db.models.sql.compiler import SQLCompiler
from django.contrib.auth.models import User

@pytest.mark.parametrize("result_type, chunked_fetch, expected", [
    (SINGLE, False, None),  # Expecting None when no results
    (MULTI, False, []),     # Expecting an empty list when no results
    (CURSOR, False, "cursor"),  # Expecting a cursor when result_type is CURSOR
])
def test_execute_sql_empty_results(result_type, chunked_fetch, expected):
    compiler = SQLCompiler(query=None, connection=connection, using=None)
    if result_type == CURSOR:
        cursor = compiler.execute_sql(result_type, chunked_fetch)
        assert cursor is not None
        cursor.close()
    else:
        result = compiler.execute_sql(result_type, chunked_fetch)
        assert result == expected

def test_execute_sql_single_result():
    user = User.objects.create(username='testuser')
    compiler = SQLCompiler(query=None, connection=connection, using=None)
    sql = f"SELECT * FROM auth_user WHERE username = 'testuser'"
    
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = compiler.execute_sql(SINGLE, False)
        assert result == (user.id, user.username, user.password, user.is_superuser)

def test_execute_sql_multi_results():
    User.objects.create(username='user1')
    User.objects.create(username='user2')

    sql = "SELECT * FROM auth_user"
    compiler = SQLCompiler(query=None, connection=connection, using=None)

    result = compiler.execute_sql(MULTI, False)
    assert len(result) >= 2  # Ensure we have at least two results