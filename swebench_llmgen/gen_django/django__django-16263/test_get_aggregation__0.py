import pytest
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.sql.query import Query


@pytest.fixture
def user_data():
    User.objects.create(username='user1', age=30)
    User.objects.create(username='user2', age=25)
    User.objects.create(username='user3', age=35)


def test_get_aggregation_no_annotations(user_data):
    query = Query(model=User, alias_cols={})
    result = query.get_aggregation(using='default', added_aggregate_names=set())
    assert result == {}


def test_get_aggregation_with_annotations(user_data):
    query = Query(model=User, alias_cols={})
    query.annotations = {'age_sum': Sum('age')}
    query.annotation_select = ['age_sum']
    
    result = query.get_aggregation(using='default', added_aggregate_names=set())
    
    # We expect the aggregation of ages (30 + 25 + 35 = 90)
    expected_result = {'age_sum': 90}
    assert result == expected_result


def test_get_aggregation_with_existing_annotations(user_data):
    query = Query(model=User, alias_cols={})
    query.annotations = {'age_sum': Sum('age')}
    query.annotation_select = ['age_sum']
    added_aggregate_names = {'age_sum'}
    
    result = query.get_aggregation(using='default', added_aggregate_names=added_aggregate_names)
    
    assert result == {'age_sum': 90}  # Should still return the correct sum, despite existing annotations.


def test_get_aggregation_with_group_by(user_data):
    query = Query(model=User, alias_cols={})
    query.group_by = ('age',)  # Simulating a grouping condition
    query.annotations = {'age_count': Count('id')}
    query.annotation_select = ['age_count']
    
    result = query.get_aggregation(using='default', added_aggregate_names=set())
    
    # Expecting number of users, since group by age will not affect that count
    assert result == {'age_count': 3}