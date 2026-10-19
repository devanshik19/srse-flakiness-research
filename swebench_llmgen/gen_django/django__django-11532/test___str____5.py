import pytest
import socket
from django.contrib.auth.models import User
from django.core.mail.utils import CachedDnsName

class TestCachedDnsName:
    def test_str_method_returns_fqdn(self, monkeypatch):
        # Arrange
        dns_name = CachedDnsName()
        
        def mock_get_fqdn():
            return "example.com"

        # Mock the get_fqdn method
        monkeypatch.setattr(dns_name, 'get_fqdn', mock_get_fqdn)

        # Act
        result = str(dns_name)

        # Assert
        assert result == "example.com"