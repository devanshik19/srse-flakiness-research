import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query
from django.db import models

class MockOptions:
    def __init__(self, db_table):
        self.db_table = db_table

def test_setup_joins_without_transforms():
    opts = MockOptions(db_table='auth_user')
    query = Query(model=User, alias_cols=False)
    alias = query.get_initial_alias()

    result = query.setup_joins(['username'], opts, alias)

    assert result.final_field == User._meta.get_field('username')  # Final field should be the username field
    assert result.opts == opts  # Options should match the input opts
    assert len(result.joins) == 1  # Only the base table should be in the joins
    assert result.joins[0] == alias  # The first alias should be equal to the one we passed in

def test_setup_joins_with_transforms():
    opts = MockOptions(db_table='auth_user')
    query = Query(model=User, alias_cols=False)
    alias = query.get_initial_alias()

    result = query.setup_joins(['username__exact'], opts, alias)

    assert result.final_field == User._meta.get_field('username')  # Final field should still refer to username
    assert result.opts == opts  # Options should still match
    assert len(result.joins) == 1  # Still expecting only the base table in the joins
    assert result.joins[0] == alias  # The first alias should remain unchanged

def test_setup_joins_reverse_foreign_key():
    class UserProfile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        bio = models.TextField()

    opts = MockOptions(db_table='auth_userprofile')
    query = Query(model=UserProfile, alias_cols=False)
    alias = query.get_initial_alias()

    with pytest.raises(AssertionError):  # as an example, this line should reflect the correct exception for reverse FK
        query.setup_joins(['user__username'], opts, alias, allow_many=False)

    result = query.setup_joins(['user__username'], opts, alias, allow_many=True)

    assert result.final_field == User._meta.get_field('username')  # Final field should still refer to the user's username
    assert result.opts == opts  # Options should match
    assert len(result.joins) > 1  # We expect joins to include at least the User table
    assert alias in result.joins  # The original alias should be included