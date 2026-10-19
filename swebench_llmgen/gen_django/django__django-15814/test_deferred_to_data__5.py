import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def query():
    user = User.objects.create(username='testuser', password='testpassword')
    return Query(model=User, alias_cols={}, deferred_loading=(['username'], True))

def test_deferred_to_data_no_field_names(query):
    target = {}
    query.deferred_loading = ([], False)
    query.deferred_to_data(target)
    assert target == {}

def test_deferred_to_data_with_fields(query):
    target = {}
    query.deferred_to_data(target)

    expected = {
        User: {'username', 'id'}
    }
    assert target == expected

def test_deferred_to_data_with_defer(query):
    target = {}
    query.deferred_loading = (['username'], True)
    query.deferred_to_data(target)

    expected = {User: {'id'}}
    assert target == expected

def test_deferred_to_data_with_must_include(query):
    # This simulates a model with an inheritance chain
    query.deferred_loading = (['username', 'profile__bio'], True)  # Assume 'profile' is a related field
    target = {}
    query.deferred_to_data(target)

    expected_user = {'username', 'id'}
    expected_profile = {'bio', 'id'}  # Assuming the profile model has these fields
    assert target[User] == expected_user
    # assert target[ProfileModel] == expected_profile   # Uncomment this when you have profile model