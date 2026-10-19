import pytest
from django.contrib.auth.models import User
from django.db.models import Field

class CustomField(Field):
    creation_counter = 0
    def __init__(self, model=None):
        self.model = model
        self.creation_counter = CustomField.creation_counter
        CustomField.creation_counter += 1

def test_field_lt():
    field_a = CustomField(model=User)
    field_b = CustomField(model=User)
    field_c = CustomField()  # No model

    # Test same creation counter, different models
    field_a.model._meta.app_label = 'app1'
    field_a.model._meta.model_name = 'model1'
    field_b.model._meta.app_label = 'app1'
    field_b.model._meta.model_name = 'model2'
    assert field_a < field_b  # field_a should be less than field_b

    # Test same model, different creation counters
    field_d = CustomField(model=User)
    field_d.creation_counter = 1  # Manually set for testing
    field_e = CustomField(model=User)
    field_e.creation_counter = 2  # Manually set for testing
    assert field_d < field_e  # field_d should be less than field_e

    # Test same creation counter, differing model existence
    assert field_c < field_a  # field_c (no model) should be less than field_a (with model)

    # Test different models with same creation counter and model presence
    field_f = CustomField(model=User)
    field_g = CustomField(model=User)
    field_f.creation_counter = 2  # Same counter
    field_g.creation_counter = 2  # Same counter

    field_f.model._meta.app_label = 'app2'
    field_f.model._meta.model_name = 'model1'
    field_g.model._meta.app_label = 'app1'
    field_g.model._meta.model_name = 'model2'

    assert field_g < field_f  # field_g should be less than field_f based on model app_label and model_name