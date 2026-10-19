import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def query_instance():
    user = User.objects.create(username='testuser', password='testpass')
    query = Query(model=user.__class__, alias_cols={})
    query.deferred_loading = (['username'], True)
    return query

def test_deferred_to_data(query_instance):
    target = {}
    query_instance.deferred_to_data(target)
    
    # Check if the target has correct model and fields included
    assert query_instance.model in target
    assert target[query_instance.model] == {'username'}
    
    # Test with no deferred loading
    query_instance.deferred_loading = ([], False)
    query_instance.deferred_to_data(target)
    
    assert target[query_instance.model] == {'username'}
    
    # Check with additional fields
    query_instance.deferred_loading = (['username', 'email'], True)
    target.clear()
    query_instance.deferred_to_data(target)

    # Assert that email is not included as it should not be loaded
    assert query_instance.model in target
    assert target[query_instance.model] == {'username'}