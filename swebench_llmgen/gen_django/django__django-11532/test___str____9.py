import pytest
from django.contrib.auth.models import User
from django.core.mail.utils import CachedDnsName

class MockCachedDnsName(CachedDnsName):
    def get_fqdn(self):
        return "example.com"

def test_cached_dns_name_str():
    dns_name = MockCachedDnsName()
    assert str(dns_name) == "example.com"