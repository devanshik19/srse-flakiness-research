import pytest
from django.contrib.auth.models import User
from django.db import models


class TestModel(User):
    related_field = models.ForeignKey(User, related_name='related_users', on_delete=models.CASCADE, null=True)


@pytest.mark.parametrize(
    'user_instance, related_user, should_raise',
    [
        (TestModel(pk=None, username='user1'), None, False),
        (TestModel(pk=None, username='user2'), User(username='related_user'), True),
        (TestModel(pk=1, username='user3'), User(pk=2, username='related_user'), False),
    ]
)
def test_prepare_related_fields_for_save(user_instance, related_user, should_raise):
    if related_user:
        related_user.save()  # Ensuring the related user is in the database if required
        user_instance.related_field = related_user

    if should_raise:
        with pytest.raises(ValueError, match=r"prohibited to prevent data loss due to unsaved related object 'related_field'."):
            user_instance._prepare_related_fields_for_save('save')
    else:
        try:
            user_instance._prepare_related_fields_for_save('save')
        except ValueError:
            pytest.fail("ValueError raised unexpectedly.")