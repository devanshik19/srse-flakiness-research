import pytest
from django.contrib.auth.models import User
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations import operations


class TestMigrationAutodetector:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.old_apps = {
            'auth': {
                'User': User
            }
        }
        
        self.new_apps = {
            'auth': {
                'User': User
            }
        }
        
        self.old_field_keys = {('auth', 'User', 'username')}
        self.new_field_keys = {('auth', 'User', 'username')}
        self.renamed_fields = {}
        self.renamed_models = {}
        self.questioner = lambda: None  # A stub for MigrationQuestioner

        # Initialize the MigrationAutodetector
        self.detector = MigrationAutodetector(self.old_apps, self.new_apps, self.questioner)

    def test_generate_altered_fields_no_changes(self):
        """Test when there are no changes in the fields"""
        self.detector.generate_altered_fields()
        assert len(self.detector.operations) == 0

    def test_generate_altered_fields_added_field(self):
        """Test adding a new field"""
        new_field = models.CharField(max_length=255, null=True)
        self.new_apps['auth']['User'].add_to_class('new_field', new_field)
        self.new_field_keys.add(('auth', 'User', 'new_field'))

        self.detector.generate_altered_fields()
        assert len(self.detector.operations) == 1
        operation = self.detector.operations[0]
        assert isinstance(operation, operations.AddField)
        assert operation.model_name == 'User'
        assert operation.name == 'new_field'

    def test_generate_altered_fields_removed_field(self):
        """Test removal of field"""
        self.new_field_keys.remove(('auth', 'User', 'username'))

        self.detector.generate_altered_fields()
        assert len(self.detector.operations) == 1
        operation = self.detector.operations[0]
        assert isinstance(operation, operations.RemoveField)
        assert operation.model_name == 'User'
        assert operation.name == 'username'

    def test_generate_altered_fields_change_field_type(self):
        """Test changing a field type"""
        new_field = models.IntegerField(null=True)
        self.new_apps['auth']['User'].add_to_class('username', new_field)

        self.detector.generate_altered_fields()
        assert len(self.detector.operations) == 1
        operation = self.detector.operations[0]
        assert isinstance(operation, operations.AlterField)
        assert operation.model_name == 'User'
        assert operation.name == 'username'

    def test_generate_altered_fields_change_remote_field(self):
        """Test changing a foreign key"""
        old_field = models.ForeignKey(User, on_delete=models.CASCADE)
        self.old_apps['auth']['User'].add_to_class('related_user', old_field)

        new_field = models.ForeignKey(User, related_name='related', on_delete=models.CASCADE)
        self.new_apps['auth']['User'].add_to_class('related_user', new_field)

        self.detector.old_field_keys.add(('auth', 'User', 'related_user'))
        self.detector.new_field_keys.add(('auth', 'User', 'related_user'))

        self.detector.generate_altered_fields()
        assert len(self.detector.operations) == 1
        operation = self.detector.operations[0]
        assert isinstance(operation, operations.AlterField)
        assert operation.model_name == 'User'
        assert operation.name == 'related_user'