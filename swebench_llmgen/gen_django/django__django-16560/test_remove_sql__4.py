import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.models.constraints import BaseConstraint

class TestBaseConstraint(BaseConstraint):

    def remove_sql(self, model, schema_editor):
        raise NotImplementedError("This method must be implemented by a subclass.")

def test_remove_sql_not_implemented():
    constraint = TestBaseConstraint()
    model = User
    schema_editor = None  # This would be a schema editor instance in a real case

    with pytest.raises(NotImplementedError, match="must be implemented by a subclass"):
        constraint.remove_sql(model, schema_editor)