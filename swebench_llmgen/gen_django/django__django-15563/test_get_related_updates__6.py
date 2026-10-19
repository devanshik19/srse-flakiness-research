import pytest
from django.contrib.auth.models import User
from django.db.models.sql.subqueries import UpdateQuery
from django.core.exceptions import FieldError

@pytest.mark.parametrize("related_updates, related_ids, expected_count", [
    ({"app_label.model_name": {"field1": "value1", "field2": "value2"}}, [1, 2, 3], 1),
    ({"app_label.model_name": {"field1": "value1"}}, None, 1),
    ({}, [1, 2, 3], 0),
])
def test_get_related_updates(related_updates, related_ids, expected_count):
    update_query = UpdateQuery()
    update_query.related_updates = related_updates
    update_query.related_ids = related_ids

    result = update_query.get_related_updates()
    
    assert len(result) == expected_count
    if expected_count > 0:
        for query in result:
            assert isinstance(query, UpdateQuery)
            assert query.values == related_updates["app_label.model_name"]
            if related_ids is not None:
                assert hasattr(query, 'related_ids')
                assert query.related_ids == related_ids