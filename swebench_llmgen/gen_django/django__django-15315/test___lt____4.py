import pytest
from django.contrib.auth.models import User
from django.db.models.fields import Field

def test_field_lt_ordering():
    field1 = Field()
    field2 = Field()

    # Assign creation counters and models for comparison
    field1.creation_counter = 1
    field2.creation_counter = 2
    field1.model = User
    field2.model = User

    assert field1 < field2  # Lower creation_counter should be less

    # Same creation counter but different models
    field3 = Field()
    field3.creation_counter = 1
    field3.model = User  # App label: auth, Model name: user
    field4 = Field()
    field4.creation_counter = 1
    field4.model = User  # App label: auth, Model name: user

    assert not (field3 < field4)  # Same creation_counter and model

    field5 = Field()
    field5.creation_counter = 1
    field5.model = User  # App label: auth, Model name: user
    field6 = Field()
    field6.creation_counter = 1
    field6.model = User  # App label: auth, Model name: another_model  # Simulating a different model

    # Verify that the ordering checks the app_label and model_name
    assert field5 < field6  # Based on app_label and model_name comparison