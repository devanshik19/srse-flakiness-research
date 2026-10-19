import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError

@pytest.mark.django_db
def test_in_bulk_with_valid_ids():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    user3 = User.objects.create(username='user3')
    
    queryset = User.objects.all()
    result = queryset.in_bulk(id_list=[user1.id, user2.id])
    
    assert result[user1.id] == user1
    assert result[user2.id] == user2
    assert user3.id not in result


@pytest.mark.django_db
def test_in_bulk_with_empty_id_list():
    queryset = User.objects.all()
    result = queryset.in_bulk(id_list=[])
    
    assert result == {}


@pytest.mark.django_db
def test_in_bulk_with_non_unique_field():
    user1 = User.objects.create(username='user1')
    
    with pytest.raises(ValueError):
        queryset = User.objects.all()
        queryset.in_bulk(id_list=[user1.id], field_name='username')


@pytest.mark.django_db
def test_in_bulk_with_id_list_exceeding_db_params():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    # Assuming the database has a limit of 1 for sample testing
    result = User.objects.in_bulk(id_list=[user1.id, user2.id])
    
    assert len(result) == 2
    assert result[user1.id] == user1
    assert result[user2.id] == user2


@pytest.mark.django_db
def test_in_bulk_with_field_name_pk():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    queryset = User.objects.all()
    result = queryset.in_bulk(id_list=[user1.id, user2.id], field_name='pk')
    
    assert result[user1.id] == user1
    assert result[user2.id] == user2