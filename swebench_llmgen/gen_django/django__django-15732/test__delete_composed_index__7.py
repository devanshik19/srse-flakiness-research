import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

class TestBaseDatabaseSchemaEditor:

    class TestModel(models.Model):
        name = models.CharField(max_length=100)
        index_name = models.Index(fields=['name'], name='name_idx')
        
        class Meta:
            indexes = [
                index_name,
            ]
    
    def setup_method(self):
        self.model = self.TestModel
        self.editor = BaseDatabaseSchemaEditor(None, collect_sql=True)
        self.editor.create_model(self.model)

    def test_delete_composed_index_success(self):
        # Ensure the index exists before deletion
        constraint_kwargs = {}
        sql = "DROP INDEX `name_idx`;"
        self.editor._delete_composed_index(self.model, ['name'], constraint_kwargs, sql)
        indexes = self.model._meta.indexes
        assert all(index.name != 'name_idx' for index in indexes)

    def test_delete_composed_index_raises_value_error_on_multiple_constraints(self):
        self.model._meta.constraints.append(
            models.UniqueConstraint(fields=['name'], name='duplicate_idx')
        )
        constraint_kwargs = {}
        sql = "DROP INDEX `name_idx`;"
        with pytest.raises(ValueError, match="Found wrong number"):
            self.editor._delete_composed_index(self.model, ['name'], constraint_kwargs, sql)

    def test_delete_composed_index_raises_value_error_on_no_constraints(self):
        constraint_kwargs = {}
        sql = "DROP INDEX `name_idx`;"
        with pytest.raises(ValueError, match="Found wrong number"):
            self.editor._delete_composed_index(self.model, ['non_existent_field'], constraint_kwargs, sql)