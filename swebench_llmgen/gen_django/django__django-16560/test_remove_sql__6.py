import warnings
import pytest
from django.core.exceptions import FieldError, ValidationError
from django.contrib.auth.models import User
from django.db import connections
from django.db.models.constraints import BaseConstraint

class TestBaseConstraint(BaseConstraint):

    def remove_sql(self, model, schema_editor):
        raise NotImplementedError("This method must be implemented by a subclass.")

def test_remove_sql_raises_not_implemented_error():
    constraint = TestBaseConstraint()
    with pytest.raises(NotImplementedError, match="This method must be implemented by a subclass."):
        constraint.remove_sql(User, connections[DEFAULT_DB_ALIAS])