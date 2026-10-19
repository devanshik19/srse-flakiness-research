import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query
from django.core.exceptions import ValueError

@pytest.mark.parametrize("field_name, value, expected_exception", [
    ("author", User.objects.all(), ValueError),
    ("author", User.objects.create(username='test_user'), None),
    ("author", [User.objects.create(username='user1'), User.objects.create(username='user2')], None),
    ("author", None, None),
])
def test_check_related_objects(field_name, value, expected_exception):
    # Prepare the Query object
    query = Query(model=User._meta.model)
    field = User._meta.get_field(field_name)
    opts = User._meta

    if expected_exception:
        with pytest.raises(expected_exception) as excinfo:
            query.check_related_objects(field, value, opts)
        assert "Cannot use QuerySet for" in str(excinfo.value)
    else:
        # When no exception is expected, just call the method
        query.check_related_objects(field, value, opts)