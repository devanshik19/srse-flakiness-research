import pytest
from django.contrib.auth.models import User
from django.db.models import F
from django.db.models.functions import Ceil

@pytest.mark.django_db
def test_as_oracle():
    user = User.objects.create(username='testuser', email='test@example.com', password='password')
    ceil_function = Ceil(F('id'))
    
    # Assuming we have an ORM setup that can compile the function
    compiler = ceil_function.get_compiler(None)
    connection = ceil_function.get_connection()
    
    sql, params = ceil_function.as_oracle(compiler, connection)
    
    assert sql == 'CEIL("auth_user"."id")'
    assert 'CEIL' in sql
    assert len(params) == 0