import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def query_with_deferred_loading():
    user_model = User._meta.concrete_model
    query = Query(user_model)
    query.defer('username', 'email')  # Example of deferred loading
    return query

def test_deferred_to_data_with_deferred_loading(query_with_deferred_loading):
    target = {}
    query_with_deferred_loading.deferred_to_data(target)
    
    user_model = User._meta.concrete_model
    assert user_model in target
    assert 'username' not in target[user_model]  # 'username' should be deferred
    assert 'email' not in target[user_model]     # 'email' should be deferred

def test_deferred_to_data_without_deferred_loading():
    user_model = User._meta.concrete_model
    query = Query(user_model)  # No deferred loading
    target = {}
    
    query.deferred_to_data(target)
    
    assert user_model in target
    assert len(target[user_model]) == len(user_model._meta.local_fields)  # All fields should be included