import socket
import pytest
from django.contrib.auth.models import User
from django.core.mail.utils import CachedDnsName

class TestCachedDnsName:
    
    def test_str_method(self, settings):
        # Mock get_fqdn method to return a specific value
        def mock_get_fqdn(self):
            return "mocked.fqdn.example.com"
        
        # Replace the get_fqdn method with our mock
        CachedDnsName.get_fqdn = mock_get_fqdn
        
        # Create an instance of the class
        cached_dns_name = CachedDnsName()
        
        # Test the __str__ method
        assert str(cached_dns_name) == "mocked.fqdn.example.com"