import pytest
from django.contrib.admin.helpers import AdminReadonlyField
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


class MockRemoteField:
    def __init__(self, model):
        self.model = model


@pytest.mark.parametrize("pk, expected", [
    (1, '<a href="/admin/auth/user/1/change/">User1</a>'),
    (2, '<a href="/admin/auth/user/2/change/">User2</a>'),
    (3, '<a href="/admin/auth/user/3/change/">User3</a>'),
])
def test_get_admin_url_existing_user(pk, expected, db):
    user = User.objects.create(username=f'User{pk}', id=pk)
    remote_field = MockRemoteField(ContentType.objects.get_for_model(User))

    readonly_field = AdminReadonlyField(None, None, None, None)
    assert readonly_field.get_admin_url(remote_field, user) == expected


def test_get_admin_url_no_reverse_match(db):
    user = User.objects.create(username='UserNoReverse', id=1000)
    remote_field = MockRemoteField(ContentType.objects.get_for_model(User))
    
    readonly_field = AdminReadonlyField(None, None, None, None)
    
    # Assuming there's no valid URL for the primary key 1000
    with pytest.raises(NoReverseMatch):
        readonly_field.get_admin_url(remote_field, user)