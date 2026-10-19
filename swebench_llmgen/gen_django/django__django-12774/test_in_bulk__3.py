import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError

@pytest.mark.django_db
def test_in_bulk_with_valid_ids():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    user3 = User.objects.create(username='user3')
    
    qs = User.objects.all()
    result = qs.in_bulk(id_list=[user1.id, user2.id])
    
    assert len(result) == 2
    assert result[user1.id] == user1
    assert result[user2.id] == user2

@pytest.mark.django_db
def test_in_bulk_with_no_ids():
    qs = User.objects.all()
    result = qs.in_bulk(id_list=None)
    
    assert isinstance(result, dict)
    assert len(result) == 0

@pytest.mark.django_db
def test_in_bulk_with_empty_ids():
    qs = User.objects.all()
    result = qs.in_bulk(id_list=[])
    
    assert isinstance(result, dict)
    assert len(result) == 0

@pytest.mark.django_db
def test_in_bulk_with_non_unique_field():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    with pytest.raises(ValueError, match="in_bulk\\(\\)'s field_name must be a unique field"):
        User.objects.all().in_bulk(id_list=[user1.id, user2.id], field_name='username')

@pytest.mark.django_db
def test_in_bulk_with_non_existent_ids():
    qs = User.objects.all()
    result = qs.in_bulk(id_list=[999, 1000])
    
    assert isinstance(result, dict)
    assert len(result) == 0

@pytest.mark.django_db
def test_in_bulk_batching_with_large_id_list():
    users = [User.objects.create(username=f'user{i}') for i in range(1, 1001)]
    id_list = [user.id for user in users]

    qs = User.objects.all()
    result = qs.in_bulk(id_list=id_list)

    assert len(result) == len(id_list)
    for user in users:
        assert result[user.id] == user