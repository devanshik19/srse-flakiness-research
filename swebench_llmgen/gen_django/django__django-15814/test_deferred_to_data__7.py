import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def query():
    # Use a valid model that has a primary key and other fields
    return Query(User)

def test_deferred_to_data_no_field_names(query):
    target = {}
    query.deferred_loading = ([], set())
    
    query.deferred_to_data(target)
    
    assert target == {}

def test_deferred_to_data_with_field_names(query):
    target = {}
    query.deferred_loading = (['username', 'email'], set())
    
    # Assuming these fields exist in the User model
    query.deferred_to_data(target)

    expected_fields = {
        User: {'username', 'email', 'id'}  # include 'id' as primary key
    }
    assert target == expected_fields

def test_deferred_to_data_with_reverse_relation(query):
    # Testing with a hypothetical reverse relationship if it existed
    # Here, we might simulate this situation by using another model.
    # However, since we are using User, this will be less relevant
    # as it doesn't have reverse relations that we can demonstrate without
    # creating new models.
    
    target = {}
    query.deferred_loading = (['groups__name'], set())
    query._filtered_relations = {'groups': User._meta.get_field('groups')}
    
    query.deferred_to_data(target)
    
    # Simulating if 'groups' related model should influence the primary key
    expected_fields = {
        User: {'id'},  # since groups is a ManyToMany, related fields aren't added
    }
    assert target == expected_fields

def test_deferred_to_data_inheritance(query):
    # Testing the inheritance chain effect on information
    target = {}
    query.deferred_loading = (['last_login'], set())

    # Simulate parent model relationship if there were one,
    # but for User model, it would just be itself.
    query.deferred_to_data(target)
    
    expected_fields = {
        User: {'last_login', 'id'}  # include 'id' as primary key from itself
    }
    assert target == expected_fields