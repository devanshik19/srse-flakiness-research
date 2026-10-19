import pytest
from django.contrib.auth.models import User
from django.core.mail.utils import CachedDnsName

class MockCachedDnsName(CachedDnsName):
    def __init__(self, fqdn):
        self._fqdn = fqdn

    def get_fqdn(self):
        return self._fqdn

def test_cached_dns_name_str():
    # Test with a regular FQDN
    dns_name = MockCachedDnsName('example.com')
    assert str(dns_name) == 'example.com'

    # Test with an FQDN that includes subdomains
    dns_name = MockCachedDnsName('sub.example.com')
    assert str(dns_name) == 'sub.example.com'

    # Test with an FQDN that includes IP address (though not a standard case)
    dns_name = MockCachedDnsName('192.168.1.1')
    assert str(dns_name) == '192.168.1.1'