import pytest
from django.contrib.auth.models import User
from django.core.mail.utils import CachedDnsName


class MockCachedDnsName(CachedDnsName):
    def get_fqdn(self):
        return "example.com"


def test_str_method_returns_fqdn():
    dns_name = MockCachedDnsName()
    assert str(dns_name) == "example.com"


def test_str_method_with_another_fqdn():
    class AnotherMockCachedDnsName(CachedDnsName):
        def get_fqdn(self):
            return "test.com"

    dns_name = AnotherMockCachedDnsName()
    assert str(dns_name) == "test.com"