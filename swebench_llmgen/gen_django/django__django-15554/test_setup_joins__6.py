import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query

@pytest.mark.parametrize("names, allow_many, expected_final_field", [
    (['profile'], True, 'profile'),  # Assuming 'profile' is a field in User model
    (['groups'], True, 'groups'),     # Assuming 'groups' is a related field
    (['nonexistent'], True, None),    # Testing for nonexistent field
    # Additional test cases can be added here based on model relations
])
def test_setup_joins(names, allow_many, expected_final_field):
    opts = User._meta
    query = Query(model=User)
    
    if expected_final_field is None:
        with pytest.raises(FieldError):
            query.setup_joins(names, opts, 'user_alias', allow_many=allow_many)
    else:
        join_info = query.setup_joins(names, opts, 'user_alias', allow_many=allow_many)
        assert join_info.final_field and expected_final_field in str(join_info.final_field)