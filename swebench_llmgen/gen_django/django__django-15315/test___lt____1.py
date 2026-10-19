import pytest
from django.contrib.auth.models import User
from django.db.models.fields import Field

@pytest.mark.django_db
def test_field_lt():
    # Create dummy fields with different creation counters and models
    field1 = Field()  # Creation counter will default to 0
    field2 = Field()  # Creation counter will default to 0

    # Set creation counters to different values
    field1.creation_counter = 1
    field2.creation_counter = 2

    assert field1 < field2  # field1 has a lower creation counter

    # Now set the same creation counter and add models
    field1.creation_counter = 2
    field2.creation_counter = 2

    # Assign models to fields
    field1.model = User
    field2.model = User

    # Should compare by the models' app_label and model_name
    assert not (field1 < field2)  # Same model should return False

    # Create another field with lower model name (assuming User has an app label)
    field3 = Field()  
    field3.creation_counter = 2
    field3.model = type('AnotherModel', (object,), {'_meta': type('Meta', (), {'app_label': 'app', 'model_name': 'another'})})

    assert field3 < field1  # field3 is alphabetically less than User