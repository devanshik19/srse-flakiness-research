import pytest
import sys
from django.core.management import ManagementUtility

class TestManagementUtility:

    def test_execute_no_arguments(self, capsys):
        argv = ['manage.py']
        utility = ManagementUtility(argv)
        utility.execute()
        captured = capsys.readouterr()
        assert 'Help' in captured.out  # Check if help text is displayed.

    def test_execute_help_command(self, capsys):
        argv = ['manage.py', 'help']
        utility = ManagementUtility(argv)
        utility.execute()
        captured = capsys.readouterr()
        assert 'Usage' in captured.out  # Check if help message is shown.

    def test_execute_version_command(self, capsys):
        argv = ['manage.py', 'version']
        utility = ManagementUtility(argv)
        utility.execute()
        captured = capsys.readouterr()
        assert f"{django.get_version()}\n" in captured.out  # Check if version is printed.

    def test_execute_invalid_command(self):
        argv = ['manage.py', 'invalid_command']
        utility = ManagementUtility(argv)
        with pytest.raises(SystemExit):  # Expecting a SystemExit on invalid command.
            utility.execute()

    def test_execute_runserver_with_autoreload(self, monkeypatch):
        argv = ['manage.py', 'runserver']
        monkeypatch.setattr('django.core.management.autoreload.check_errors', lambda func: func)
        utility = ManagementUtility(argv)
        utility.execute()
        # Since we can't capture the output from an internal call, we assume no errors.

    def test_execute_runserver_without_autoreload(self, monkeypatch):
        argv = ['manage.py', 'runserver', '--noreload']
        monkeypatch.setattr('django.core.management.autoreload.check_errors', lambda func: func)
        utility = ManagementUtility(argv)
        utility.execute()
        # Assuming no exceptions raise.

    def test_execute_help_with_commands_flag(self, capsys):
        argv = ['manage.py', 'help', '--commands']
        utility = ManagementUtility(argv)
        utility.execute()
        captured = capsys.readouterr()
        assert 'Available commands' in captured.out  # Check if command list is displayed.