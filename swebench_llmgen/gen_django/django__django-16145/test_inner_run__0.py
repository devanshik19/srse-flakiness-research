import errno
import os
import sys
import pytest
from django.conf import settings
from django.core.management import CommandError
from django.core.management.commands.runserver import Command

class TestCommand:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.command = Command()
        self.command.addr = '127.0.0.1'
        self.command.port = '8000'
        self.command.protocol = 'http'
        self.command.stdout = type('Dummy', (object,), {'write': lambda s, msg: None})
        self.command.stderr = type('Dummy', (object,), {'write': lambda s, msg: None})

    def test_inner_run_without_errors(self, monkeypatch):
        monkeypatch.setattr(self.command, 'check_migrations', lambda: None)
        monkeypatch.setattr(self.command, 'get_handler', lambda *args, **options: lambda environ, start_response: None)
        monkeypatch.setattr(self.command, 'get_version', lambda: '3.2.0')
        monkeypatch.setattr(settings, 'SETTINGS_MODULE', 'mysite.settings')

        options = {
            'use_threading': True,
            'skip_checks': False,
            'shutdown_message': ''
        }

        self.command.inner_run([], options)

    def test_inner_run_with_oserror_permissions(self, monkeypatch):
        def raise_oserror(*args, **kwargs):
            raise OSError(errno.EACCES, 'Permission denied')

        monkeypatch.setattr(self.command, 'check_migrations', lambda: None)
        monkeypatch.setattr(self.command, 'get_handler', raise_oserror)

        options = {
            'use_threading': True,
            'skip_checks': False,
            'shutdown_message': ''
        }

        with pytest.raises(SystemExit):
            self.command.inner_run([], options)

    def test_inner_run_with_oserror_address_in_use(self, monkeypatch):
        def raise_oserror(*args, **kwargs):
            raise OSError(errno.EADDRINUSE, 'Address already in use')

        monkeypatch.setattr(self.command, 'check_migrations', lambda: None)
        monkeypatch.setattr(self.command, 'get_handler', raise_oserror)

        options = {
            'use_threading': True,
            'skip_checks': False,
            'shutdown_message': ''
        }

        with pytest.raises(SystemExit):
            self.command.inner_run([], options)

    def test_inner_run_with_keyboard_interrupt(self, monkeypatch):
        def raise_keyboard_interrupt(*args, **kwargs):
            raise KeyboardInterrupt()

        monkeypatch.setattr(self.command, 'check_migrations', lambda: None)
        monkeypatch.setattr(self.command, 'get_handler', raise_keyboard_interrupt)

        options = {
            'use_threading': True,
            'skip_checks': False,
            'shutdown_message': 'Shutting down the server...'
        }

        with pytest.raises(SystemExit):
            self.command.inner_run([], options)