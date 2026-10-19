import pytest
from django.contrib.auth.models import User
from django.db.models.query_utils import RegisterLookupMixin

class TestRegisterLookupMixin(RegisterLookupMixin):
    class_lookups = {}

    @classmethod
    def register_lookup(cls, lookup, lookup_name):
        cls.class_lookups[lookup_name] = lookup

@pytest.fixture
def setup_lookups():
    TestRegisterLookupMixin.register_lookup(lambda x: x, 'custom_lookup')
    yield
    # Cleanup after the test
    if 'custom_lookup' in TestRegisterLookupMixin.class_lookups:
        del TestRegisterLookupMixin.class_lookups['custom_lookup']

def test_unregister_lookup_existing(setup_lookups):
    assert 'custom_lookup' in TestRegisterLookupMixin.class_lookups
    TestRegisterLookupMixin._unregister_lookup(TestRegisterLookupMixin, lambda x: x, 'custom_lookup')
    assert 'custom_lookup' not in TestRegisterLookupMixin.class_lookups

def test_unregister_lookup_nonexistent(setup_lookups):
    assert 'custom_lookup' in TestRegisterLookupMixin.class_lookups
    TestRegisterLookupMixin._unregister_lookup(TestRegisterLookupMixin, lambda x: x, 'nonexistent_lookup')
    # Ensure the existing lookup is still there
    assert 'custom_lookup' in TestRegisterLookupMixin.class_lookups