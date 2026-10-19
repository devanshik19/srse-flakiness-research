import pytest
from django.db.models import QuerySet
from django.contrib.auth.models import User

def test_set_values():
    # Prepare a QuerySet from the User model
    queryset = User.objects.all()
    
    # Use Query instance to create a Query object
    query = queryset.query

    # Test case when fields are specified
    fields = ['id', 'username', 'email']
    query.set_values(fields)
    
    # Check if values_select has been set correctly
    assert query.values_select == ('id', 'username', 'email')
    
    # Check internal states after setting values
    assert not query.select_related
    assert not query.default_cols
    assert query.extra_select_mask is None
    assert query.annotation_select_mask is None

    # Test case when extra and annotations are also set
    query.extra_select = {'extra_field': 'COUNT(*)'}
    query.annotation_select = {'annotation_field': 'MAX(id)'}
    fields = ['extra_field', 'annotation_field', 'first_name']
    
    query.set_values(fields)
    
    assert query.values_select == ('extra_field', 'annotation_field', 'first_name')
    assert 'extra_field' in query.extra_select
    assert 'annotation_field' in query.annotation_select
    
    # Testing the edge case where no fields are provided
    query.set_values([])
    
    expected_fields = [f.attname for f in User._meta.concrete_fields]
    assert query.values_select == tuple(expected_fields)

    # Test with a specific group_by condition
    query.group_by = True
    query.set_values(['username'])
    
    assert query.group_by is False  # Group by should be reset
    assert query.values_select == ('username',)
    
    # Verify the internal state is consistent after resetting
    assert query.select == ('username',)  # assuming query.select gets updated