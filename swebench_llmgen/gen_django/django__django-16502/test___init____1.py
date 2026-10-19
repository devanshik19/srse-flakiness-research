import pytest
import socket
from django.core.servers.basehttp import WSGIServer


class TestWSGIServer:

    def test_init_with_ipv6(self):
        server = WSGIServer(ipv6=True)
        assert server.address_family == socket.AF_INET6
        assert server.allow_reuse_address is True

    def test_init_without_ipv6(self):
        server = WSGIServer()
        assert server.address_family == socket.AF_INET
        assert server.allow_reuse_address is True

    def test_init_with_allow_reuse_address_false(self):
        server = WSGIServer(allow_reuse_address=False)
        assert server.allow_reuse_address is False

    def test_init_with_args_and_kwargs(self):
        server = WSGIServer(1234, allow_reuse_address=True)
        assert server.allow_reuse_address is True