import pytest
from django.contrib.auth.models import User
from django.core.mail.utils import CachedDnsName

class TestCachedDnsName:
    @pytest.fixture
    def cached_dns_name(self):
        instance = CachedDnsName()
        instance.get_fqdn = lambda: "example.com"  # Mocking get_fqdn return value
        return instance

    def test_str(self, cached_dns_name):
        assert str(cached_dns_name) == "example.com"