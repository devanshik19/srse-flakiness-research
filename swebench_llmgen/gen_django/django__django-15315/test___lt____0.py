import pytest
from django.contrib.auth.models import User
from django.db.models import Field

@pytest.mark.django_db
def test_field_lt():
    # Create two Field instances with different creation counters
    field1 = Field()
    field2 = Field()
    field1.creation_counter = 1
    field2.creation_counter = 2
    
    assert field1 < field2  # field1 should be less than field2 due to lower creation_counter

    # Create two Field instances with the same creation counter but different models
    field1.creation_counter = 1
    field2.creation_counter = 1
    field1.model = User
    field2.model = User
    
    # Test ordering by model when creation counters are equal
    assert field1 >= field2  # Same models, should not be less than
    
    # Change models for field2 to check model ordering
    field2.model = None
    
    # Check that field1 (having model) is greater than field2 (no model)
    assert field1 > field2
    
    # Testing with non-Field type
    non_field = "not_a_field"
    assert field1.__lt__(non_field) is NotImplemented