import pytest
from django.contrib.auth.models import User
from django.utils.dateformat import DateFormat

def test_y():
    # Test for a typical year
    user = User.objects.create(username='testuser', date_joined=datetime.datetime(2020, 1, 1))
    df = DateFormat()
    df.data = user.date_joined
    assert df.y() == '20'
    
    # Test for year 1999
    user2 = User.objects.create(username='testuser2', date_joined=datetime.datetime(1999, 12, 31))
    df2 = DateFormat()
    df2.data = user2.date_joined
    assert df2.y() == '99'
    
    # Test for year 2001
    user3 = User.objects.create(username='testuser3', date_joined=datetime.datetime(2001, 5, 15))
    df3 = DateFormat()
    df3.data = user3.date_joined
    assert df3.y() == '01'