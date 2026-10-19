import errno
import os
import sys
import pytest
from django.core.management import CommandError
from django.core.management.commands.runserver import Command

class TestCommand:
    
    def test_inner_run_success(self, monkeypatch, capsys):
        command = Command()
        command.addr = '127.0.0.1'
        command.port = 8000
        command.protocol = 'http'
        command.use_ipv6 = False
        command.stdout = sys.stdout
        command.stderr = sys.stderr
        
        # Mocking get_handler method
        def mock_get_handler(*args, **options):
            return lambda environ, start_response: start_response(b'200 OK', [(b'Content-Type', b'text/plain')])(b'Hello World')

        monkeypatch.setattr(command, 'get_handler', mock_get_handler)

        options = {
            'use_threading': True,
            'shutdown_message': '',
        }
        command.inner_run([], options)

        captured = capsys.readouterr()
        assert "Performing system checks..." in captured.out
        assert "Django version" in captured.out
        assert "Starting development server" in captured.out

    def test_inner_run_os_error(self, monkeypatch, capsys):
        command = Command()
        command.addr = '127.0.0.1'
        command.port = 8000
        command.protocol = 'http'
        command.use_ipv6 = False
        
        # Simulating an error when running the server
        monkeypatch.setattr(os, '_exit', lambda code: None)  # Prevent exit during the test
        monkeypatch.setattr(command, 'get_handler', lambda *args, **options: 1/0)  # Will raise ZeroDivisionError first

        options = {
            'use_threading': True,
            'shutdown_message': '',
        }
        
        with pytest.raises(SystemExit):  # Expecting system exit due to OSError in run
            command.inner_run([], options)

        captured = capsys.readouterr()
        assert "Error:" in captured.stderr

    def test_inner_run_keyboard_interrupt(self, monkeypatch):
        command = Command()

        # Simulating KeyboardInterrupt
        monkeypatch.setattr(command, 'get_handler', lambda *args, **options: (_ for _ in ()).throw(KeyboardInterrupt))

        options = {
            'use_threading': True,
            'shutdown_message': '',
        }

        with pytest.raises(SystemExit):  # Expecting system exit due to KeyboardInterrupt
            command.inner_run([], options)