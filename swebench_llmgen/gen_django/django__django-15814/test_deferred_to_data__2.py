import copy
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_deferred_to_data():
    # Create a Query object for User model with deferred loading
    query = Query(model=User)
    query.add_deferred_loading(['username', 'email'])

    # Prepare a target dictionary to hold the results
    target = {}

    # Call the deferred_to_data method
    query.deferred_to_data(target)

    # Assert that the target contains the appropriate models and fields
    assert User in target
    assert 'username' not in target[User]
    assert 'email' not in target[User]
    
    # Check if pk and other fields are included
    assert 'id' in target[User]  # Ensure primary key is included
    assert 'first_name' in target[User]  # Other fields should be included by default
    assert 'last_name' in target[User]
    
    # Now check the behavior when no fields are deferred
    query.clear_deferred_loading()  # Remove any deferred fields
   
    # Call the deferred_to_data method again
    target = {}
    query.deferred_to_data(target)

    # Assert that all fields are in the target now since none are deferred
    assert User in target
    assert len(target[User]) == len(User._meta.fields)  # All fields should be included