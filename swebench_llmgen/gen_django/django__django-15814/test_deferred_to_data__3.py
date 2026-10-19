import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

# Helper function to add to the dictionary
def add_to_dict(target_dict, key, value):
    if key not in target_dict:
        target_dict[key] = set()
    target_dict[key].add(value)

def is_reverse_o2o(field):
    return False  # Placeholder for the actual implementation used in the original code

# Test class that extends Query
class TestQuery(Query):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deferred_loading = (['username', 'email'], False)
        self.model = User
        
    def get_meta(self):
        return self.model._meta

# Test cases for deferred_to_data
@pytest.mark.parametrize("defer", [True, False])
@pytest.mark.parametrize("field_names", [
    (['username', 'email']), 
    (['username']), 
    (['nonexistent_field']),
    ([])  # Test empty case
])
def test_deferred_to_data(field_names, defer):
    # Prepare the target dict
    target = {}
    
    # Create an instance of TestQuery with simulated deferred_loading
    query = TestQuery(model=User)
    query.deferred_loading = (field_names, defer)
    query._filtered_relations = {}

    # Call the method under test
    query.deferred_to_data(target)
    
    # Assert resulting structure in target
    if not field_names:
        assert target == {}
    else:
        expected_keys = {User}
        if defer:
            # When defer is True, we should see fields not in field_names
            expected_fields = {f.attname for f in User._meta.local_fields if f.name not in field_names}
        else:
            # When defer is False, we should see the must_include fields only
            expected_fields = {f.attname for f in User._meta.local_fields}

        assert target.keys() == expected_keys
        assert target[User] == expected_fields