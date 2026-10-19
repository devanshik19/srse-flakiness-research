import pytest
from django.contrib.auth.models import User
from django.db import schema
from django.db.models.constraints import BaseConstraint

class TestBaseConstraint(BaseConstraint):

    def remove_sql(self, model, schema_editor):
        raise NotImplementedError("This method must be implemented by a subclass.")

def test_remove_sql_not_implemented():
    constraint = TestBaseConstraint()
    model = User
    schema_editor = schema.schema_editor()

    with pytest.raises(NotImplementedError, match="This method must be implemented by a subclass."):
        constraint.remove_sql(model, schema_editor)