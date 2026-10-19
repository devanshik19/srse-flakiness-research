import pytest
from django.contrib.auth.models import User
from django.db.models import Q

@pytest.mark.parametrize("children, connector, negated, expected", [
    ([(User._meta.get_field('username').name, 'testuser')], None, False, 
     ('django.db.models.Q', ('username', 'testuser'), {})),
    ([(User._meta.get_field('username').name, 'testuser')], Q.AND, False, 
     ('django.db.models.Q', ('username', 'testuser'), {'_connector': Q.AND})),
    ([(User._meta.get_field('username').name, 'testuser'), (User._meta.get_field('email').name, 'test@example.com')], None, False,
     ('django.db.models.Q', (('username', 'testuser'), ('email', 'test@example.com')), {})),
    ([(User._meta.get_field('username').name, 'testuser')], None, True, 
     ('django.db.models.Q', ('username', 'testuser'), {'_negated': True})),
])
def test_deconstruct(children, connector, negated, expected):
    q_instance = Q(*children)
    q_instance.connector = connector if connector else Q.AND
    q_instance.negated = negated
    path, args, kwargs = q_instance.deconstruct()
    assert (path, args, kwargs) == expected