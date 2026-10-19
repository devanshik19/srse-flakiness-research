import pytest
from django.contrib.auth.models import User
from django.db.models import Value, F
from django.db.models.sql.query import Query

def test_output_field_single_select():
    # Create a query object
    query = Query(model=User)

    # Simulate a single select field
    query.select = [F('username')]
    
    # Call the output_field method
    result = query.output_field()
    
    # Assert the result is as expected (should return the field)
    assert result == User._meta.get_field('username')

def test_output_field_single_annotation_select():
    # Create a query object
    query = Query(model=User)

    # Simulate a single annotation select
    query.annotation_select = {'count': Value(Count('id'))}

    # Call the output_field method
    result = query.output_field()

    # Assert the result is as expected (should return the output field of the annotation)
    assert result is not None  # Check if output_field exists on the annotation

def test_output_field_multiple_selects():
    # Create a query object
    query = Query(model=User)

    # Simulate multiple select fields
    query.select = [F('username'), F('email')]

    # Call the output_field method
    result = query.output_field()

    # Assert that result is None since there are multiple selects
    assert result is None

def test_output_field_multiple_annotations():
    # Create a query object
    query = Query(model=User)

    # Simulate multiple annotation selects
    query.annotation_select = {
        'count': Value(Count('id')),
        'avg_age': Value(30)
    }

    # Call the output_field method
    result = query.output_field()

    # Assert that result is None since there are multiple annotations
    assert result is None