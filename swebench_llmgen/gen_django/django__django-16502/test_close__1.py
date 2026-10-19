import pytest
import io
from django.contrib.auth.models import User
from django.core.servers.basehttp import ServerHandler

class TestServerHandler:

    @pytest.fixture
    def server_handler(self):
        stdin = io.StringIO("Test Input\n")
        stdout = io.StringIO()
        stderr = io.StringIO()
        environ = {}
        handler = ServerHandler(stdin, stdout, stderr, environ)
        return handler

    def test_close_reads_stdin_and_calls_super_close(self, server_handler):
        # Arrange
        server_handler.get_stdin = lambda: io.StringIO("Test Input\n")
        super_close_called = False

        # Mock the super().close() method
        original_super_close = ServerHandler.close
        def mock_super_close(self):
            nonlocal super_close_called
            super_close_called = True

        # Replace the close method temporarily
        ServerHandler.close = mock_super_close.__get__(server_handler)

        # Act
        server_handler.close()

        # Assert
        assert super_close_called
        assert server_handler.get_stdin().read() == "Test Input\n"

        # Restore the original close method
        ServerHandler.close = original_super_close