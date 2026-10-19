import pytest
from django.db.models import Aggregate

class CustomAggregate(Aggregate):
    def __init__(self, *args, distinct=False, filter=None, **kwargs):
        self.distinct = distinct
        self.filter = filter
        super().__init__(*args, **kwargs)

    def _get_repr_options(self):
        options = super()._get_repr_options()
        if self.distinct:
            options['distinct'] = self.distinct
        if self.filter:
            options['filter'] = self.filter
        return options

def test_get_repr_options():
    # Test case when neither distinct nor filter is set
    aggregate = CustomAggregate()
    options = aggregate._get_repr_options()
    assert options == {}

    # Test case when distinct is set to True
    aggregate = CustomAggregate(distinct=True)
    options = aggregate._get_repr_options()
    assert options == {'distinct': True}

    # Test case when filter is set
    aggregate = CustomAggregate(filter='some_filter')
    options = aggregate._get_repr_options()
    assert options == {'filter': 'some_filter'}

    # Test case when both distinct and filter are set
    aggregate = CustomAggregate(distinct=True, filter='some_filter')
    options = aggregate._get_repr_options()
    assert options == {'distinct': True, 'filter': 'some_filter'}