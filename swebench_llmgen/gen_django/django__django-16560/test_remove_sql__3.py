import pytest
from django.db import schema
from django.contrib.auth.models import User
from django.db.models.constraints import BaseConstraint

class TestBaseConstraint(BaseConstraint):
    def constraint_sql(self, model, schema_editor):
        return "SELECT 1"

    def create_sql(self, model, schema_editor):
        return "CREATE CONSTRAINT"

    def validate(self, model, instance, exclude, using):
        pass


def test_remove_sql_raises_notimplementederror():
    constraint = TestBaseConstraint()

    with pytest.raises(NotImplementedError, match="This method must be implemented by a subclass."):
        constraint.remove_sql(User, None)