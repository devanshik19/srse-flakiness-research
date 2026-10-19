import pytest
from django.db.models import F, Expression
from django.contrib.auth.models import User
from django.db import connection


class TestBaseExpression(Expression):
    def __init__(self, output_field):
        super().__init__(output_field)

    def as_sql(self, compiler, connection):
        return 'SELECT *', []


def test_as_sql_not_implemented():
    base_expression = BaseExpression(output_field=None)
    with pytest.raises(NotImplementedError):
        base_expression.as_sql(None, None)


def test_as_sql_implemented():
    test_expression = TestBaseExpression(output_field=None)
    sql, params = test_expression.as_sql(None, connection)
    assert sql == 'SELECT *'
    assert params == []


@pytest.mark.django_db
def test_as_sql_with_user_model():
    user_expression = TestBaseExpression(output_field=None)
    sql, params = user_expression.as_sql(None, connection)
    user = User.objects.create_user(username='testuser', password='password')
    assert user.username == 'testuser'
    assert sql == 'SELECT *'
    assert params == []