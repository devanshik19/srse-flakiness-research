import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.mark.parametrize("fields, expected_values_select", [
    (['username', 'email'], ('username', 'email')),
    (['first_name', 'last_name'], ('first_name', 'last_name')),
    ([], ('username', 'email', 'first_name', 'last_name')),  # Testing default fields when fields is empty
])
def test_set_values(fields, expected_values_select):
    query = Query(User)
    
    # Setting up extra select and annotation for testing
    query.extra_select = {}
    query.annotation_select = {}
    
    # Call the focal function set_values
    query.set_values(fields)
    
    # Verify that the values_select attribute matches the expected outcome
    assert query.values_select == expected_values_select

def test_set_values_with_extra_and_annotation():
    query = Query(User)
    query.extra_select = {'extra_field': 'extra_column'}
    query.annotation_select = {'annotated_field': 'annotated_column'}
    
    fields = ['username', 'extra_field', 'annotated_field']
    query.set_values(fields)
    
    expected_values_select = ('username', 'extra_field', 'annotated_field')
    assert query.values_select == expected_values_select

def test_set_values_group_by_behavior():
    query = Query(User)
    query.group_by = True  # Set group_by to True
    
    fields = ['username']
    query.set_values(fields)
    
    expected_values_select = ('username',)
    assert query.values_select == expected_values_select
    assert query.group_by is False  # The group_by should be disabled

def test_set_values_with_nonexistent_field():
    query = Query(User)
    fields = ['nonexistent_field']  # Testing with non existent field
    
    with pytest.raises(FieldDoesNotExist):
        query.set_values(fields)