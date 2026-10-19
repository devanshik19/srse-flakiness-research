import pytest
from django.db.models import F
from django.contrib.auth.models import User
from django.db import connections
from django.core.exceptions import ValidationError
from django.db.models.constraints import BaseConstraint

class TestBaseConstraint(BaseConstraint):
    def create_sql(self, model, schema_editor):
        return "CREATE SQL"

    def remove_sql(self, model, schema_editor):
        raise NotImplementedError("This method must be implemented by a subclass.")

def test_remove_sql_not_implemented():
    constraint = TestBaseConstraint()
    model = User
    schema_editor = connections[DEFAULT_DB_ALIAS].schema_editor()

    with pytest.raises(NotImplementedError, match="must be implemented by a subclass"):
        constraint.remove_sql(model, schema_editor)