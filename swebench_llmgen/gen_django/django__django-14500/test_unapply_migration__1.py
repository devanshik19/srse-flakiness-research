import pytest
from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations import Migration
from django.db.migrations.recorder import MigrationRecorder
from django.db.migrations.state import ProjectState
from django.test import TestCase

User = get_user_model()

class TestMigrationExecutor(TestCase):
    def setUp(self):
        self.connection = connection
        self.recorder = MigrationRecorder(self.connection)
        self.progress_callback = None
        self.executor = MigrationExecutor(self.connection, self.progress_callback)
        
        # Create a test user and apply an initial migration.
        User.objects.create_user(username='testuser', password='password')
        self.state = ProjectState()
        
        # Assume the initial migration is recorded
        self.migration = Migration('0001_initial', 'auth')
        self.executor.recorder.record_applied('auth', '0001_initial')
        
    def test_unapply_migration_fake(self):
        state_after_unapply = self.executor.unapply_migration(self.state, self.migration, fake=True)

        assert state_after_unapply == self.state  # state should remain unchanged
        assert self.recorder.has_unapplied('auth', '0001_initial')  # the migration should be recorded as unapplied

    def test_unapply_migration_real(self):
        # First, apply the migration
        self.executor.apply_migration(self.state, self.migration)
        
        # Now unapply the migration
        state_after_unapply = self.executor.unapply_migration(self.state, self.migration, fake=False)

        assert state_after_unapply == self.state  # Check that state is as expected
        assert not User.objects.filter(username='testuser').exists()  # Ensure the user was deleted
        assert self.recorder.has_unapplied('auth', '0001_initial')  # Check if the migration is recorded as unapplied

    def test_unapply_migration_with_replacement(self):
        # Setting up a mock migration that has replacements
        self.migration.replaces = [('auth', '0001_initial')]
        
        # Apply the migration first
        self.executor.apply_migration(self.state, self.migration)
        
        # Unapply it
        state_after_unapply = self.executor.unapply_migration(self.state, self.migration, fake=False)

        assert state_after_unapply == self.state  # State should match
        assert self.recorder.has_unapplied('auth', '0001_initial')  # Replacement should record the old migration