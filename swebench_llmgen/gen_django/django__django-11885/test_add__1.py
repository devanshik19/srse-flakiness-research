import pytest
from django.contrib.auth.models import User
from django.db.models.deletion import Collector

@pytest.mark.parametrize("objs, source, nullable, reverse_dependency, expected", [
    ([], None, False, False, []),
    ([User(username='user1'), User(username='user2')], None, False, False, 
     [User(username='user1'), User(username='user2')]),
    ([User(username='user1'), User(username='user1')], None, False, False, 
     [User(username='user1')]),
    ([User(username='user1')], None, False, True, 
     [User(username='user1')]),
    ([User(username='user1'), User(username='user2')], User, False, False, 
     [User(username='user1'), User(username='user2')]),
])
def test_add(objs, source, nullable, reverse_dependency, expected):
    collector = Collector(using='default')

    if source is not None:
        # Ensure the source is a valid User instance for the test
        source = User(username='source_user')
        source.save()

    # Save objects to database first to prevent IntegrityError when adding
    user_objs = [User(username=obj.username) for obj in objs] if objs else []
    for user in user_objs:
        user.save()

    results = collector.add(user_objs, source=source, nullable=nullable, reverse_dependency=reverse_dependency)
    
    assert results == expected
    if expected and source is not None and not nullable:
        assert source in collector.dependencies
        assert User in collector.dependencies[source._meta.concrete_model]
    else:
        assert source not in collector.dependencies