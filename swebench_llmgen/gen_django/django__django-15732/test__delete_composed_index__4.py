import pytest
from django.db import models
from django.contrib.auth.models import User
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

class TestDatabaseSchemaEditor:
    @pytest.fixture
    def schema_editor(self, connection):
        return BaseDatabaseSchemaEditor(connection=connection, collect_sql=True)

    @pytest.fixture
    def create_composed_index(self, schema_editor):
        class TestModel(models.Model):
            username = models.CharField(max_length=30)
            email = models.EmailField()
        
        TestModel._meta.constraints = [
            models.UniqueConstraint(fields=['username', 'email'], name='uc_username_email')
        ]
        
        schema_editor.add_constraint(TestModel, TestModel._meta.constraints[0])
        yield TestModel
        schema_editor.remove_constraint(TestModel, TestModel._meta.constraints[0])

    def test_delete_composed_index_success(self, schema_editor, create_composed_index):
        model = create_composed_index
        fields = ['username', 'email']
        sql = 'ALTER TABLE "app_testmodel" DROP CONSTRAINT "uc_username_email";'

        # Execute the delete composed index function
        schema_editor._delete_composed_index(model, fields, {}, sql)

        # Assert the constraint has been removed
        constraint_names = schema_editor._constraint_names(
            model, 
            [model._meta.get_field(field).column for field in fields]
        )
        assert len(constraint_names) == 0

    def test_delete_composed_index_wrong_number_of_constraints(self, schema_editor, create_composed_index):
        model = create_composed_index
        fields = ['username', 'email']
        sql = 'ALTER TABLE "app_testmodel" DROP CONSTRAINT "uc_username_email";'

        # Add two constraints to trigger the error condition
        schema_editor.add_constraint(model, models.UniqueConstraint(fields=['username'], name='uc_username'))
        schema_editor.add_constraint(model, models.UniqueConstraint(fields=['email'], name='uc_email'))

        with pytest.raises(ValueError) as exc_info:
            schema_editor._delete_composed_index(model, fields, {}, sql)

        assert "Found wrong number" in str(exc_info.value)
        assert model._meta.db_table in str(exc_info.value)