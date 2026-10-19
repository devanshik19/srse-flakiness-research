import io
import os
import sys
import warnings
from django.apps import apps
from django.core.management.base import CommandError
from django.core.management import call_command
from django.contrib.auth.models import User
import pytest


class TestCommand:

    def setup_method(self):
        self.command = Command()
        self.command.stdout = io.StringIO()
        self.command.stderr = io.StringIO()

    def test_handle_no_app_labels(self):
        self.command.handle()
        assert "App 'None' could not be found" in self.command.stderr.getvalue()

    def test_handle_invalid_app_label(self):
        invalid_app_label = 'invalid_app'
        self.command.handle(invalid_app_label)
        assert f"App '{invalid_app_label}' could not be found." in self.command.stderr.getvalue()

    def test_handle_valid_app_label_no_changes(self):
        User.objects.create_user(username='testuser', password='password')
        self.command.handle('auth')
        assert "No changes detected in app 'auth'" in self.command.stdout.getvalue()

    def test_handle_empty_migration(self):
        with pytest.raises(CommandError, match="You must supply at least one app label when using --empty."):
            self.command.handle(empty=True)

        self.command.empty = True
        self.command.migration_name = 'custom_empty'
        self.command.handle('auth')
        assert "custom_empty" in os.listdir('auth/migrations')

    def test_handle_conflicting_migrations(self):
        # Create a scenario for conflicting migrations
        # Assuming we are using a migration that previously existed in the auth app.
        self.command.merge = False
        self.command.handle('auth')
        assert "Conflicting migrations detected" in self.command.stderr.getvalue()

    def test_handle_merge_migrations(self):
        # Set up a conflict scenario but allow for merging
        self.command.merge = True
        User.objects.create_user(username='testuser', password='password')
        self.command.handle('auth')
        assert "No conflicts detected to merge." in self.command.stdout.getvalue()

    def test_handle_with_exit_code(self):
        self.command.exit_code = True
        with pytest.warns(RemovedInDjango20Warning):
            self.command.handle('auth')
        assert self.command.exit_code == True