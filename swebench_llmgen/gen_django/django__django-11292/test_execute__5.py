import pytest
from django.core.management.base import BaseCommand
from django.core.management import CommandError
from django.contrib.auth.models import User
from io import StringIO

class TestBaseCommand(BaseCommand):
    def setup_method(self):
        self.stdout = StringIO()
        self.stderr = StringIO()
        self.command = BaseCommand(stdout=self.stdout, stderr=self.stderr, no_color=True, force_color=False)
        self.command.requires_system_checks = True
        self.command.requires_migrations_checks = True

    def test_execute_with_no_color(self):
        options = {'no_color': True, 'force_color': False, 'skip_checks': False}
        result = self.command.execute('test_args', **options)
        assert result is None

    def test_execute_with_force_color(self):
        options = {'no_color': False, 'force_color': True, 'skip_checks': False}
        result = self.command.execute('test_args', **options)
        assert result is None
        assert self.command.style.force_color is True

    def test_execute_conflicting_options(self):
        options = {'no_color': True, 'force_color': True, 'skip_checks': False}
        with pytest.raises(CommandError, match="The --no-color and --force-color options can't be used together."):
            self.command.execute('test_args', **options)

    def test_execute_with_stdout_and_stderr(self):
        options = {'no_color': True, 'force_color': False, 'skip_checks': False, 'stdout': StringIO(), 'stderr': StringIO()}
        output = self.command.execute('test_args', **options)
        assert output is None
        assert isinstance(self.command.stdout, StringIO)
        assert isinstance(self.command.stderr, StringIO)

    def test_execute_without_system_checks(self):
        options = {'no_color': True, 'force_color': False, 'skip_checks': True}
        result = self.command.execute('test_args', **options)
        assert result is None

    def test_execute_with_migrations_check(self):
        options = {'no_color': True, 'force_color': False, 'skip_checks': False}
        result = self.command.execute('test_args', **options)
        assert result is None

    def test_execute_outputs_when_handling(self):
        def mock_handle(*args, **options):
            return "Handled output"
        
        self.command.handle = mock_handle
        options = {'no_color': True, 'force_color': False, 'skip_checks': False}
        self.command.output_transaction = False
        result = self.command.execute('test_args', **options)
        assert result == "Handled output"
        assert self.stdout.getvalue() == "Handled output\n"