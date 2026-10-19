import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

class MockSchemaEditor(BaseDatabaseSchemaEditor):
    def execute(self, sql, params=None):
        pass
    
    def _delete_composed_index(self, model, fields, constraint_kwargs, sql):
        pass

    def _create_unique_sql(self, model, fields):
        return f"CREATE UNIQUE INDEX ON {model._meta.db_table}({', '.join(field.name for field in fields)})"

def test_alter_unique_together():
    old_unique_together = [['username']]
    new_unique_together = [['username'], ['email']]

    editor = MockSchemaEditor(connection, collect_sql=False, atomic=False)

    user_model = User

    # Mock deletions
    editor._delete_composed_index = lambda model, fields, constraint_kwargs, sql: assert fields == ('username', )

    # Capture the SQL executed
    executed_sqls = []

    def patch_execute(sql, params=None):
        executed_sqls.append(sql)

    editor.execute = patch_execute

    # Call the method to test
    editor.alter_unique_together(user_model, old_unique_together, new_unique_together)

    # Check that deletion of old unique together happened
    assert len(executed_sqls) == 1
    assert executed_sqls[0] == "CREATE UNIQUE INDEX ON auth_user(email)"

    # Reset for new uniques
    executed_sqls.clear()

    # Call the method again with only the new unique
    editor.alter_unique_together(user_model, new_unique_together, [['email']])

    # Confirm that it handled correctly
    assert len(executed_sqls) == 0