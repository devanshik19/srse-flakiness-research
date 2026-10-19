import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def query_instance():
    user = User.objects.create(username='testuser', password='testpass')
    query = Query(model=User, alias_cols={})
    query.deferred_loading = (['username'], True)  # Simulating deferred loading for the 'username' field
    return query

def test_deferred_to_data_with_defer(query_instance):
    target = {}
    query_instance.deferred_to_data(target)
    assert target[User] == {'username'}

def test_deferred_to_data_without_defer(query_instance):
    query_instance.deferred_loading = (['username'], False)  # No deferring
    target = {}
    query_instance.deferred_to_data(target)
    assert User._meta.pk.attname in target[User]  # Check that primary key is included

def test_deferred_to_data_with_no_fields(query_instance):
    query_instance.deferred_loading = ([], True)  # No fields to defer
    target = {}
    query_instance.deferred_to_data(target)
    assert target == {}  # Should return an empty target

def test_deferred_to_data_with_missing_field(query_instance):
    query_instance.deferred_loading = (['non_existing_field'], True)  # Simulating a missing field
    target = {}
    with pytest.raises(FieldDoesNotExist):
        query_instance.deferred_to_data(target)