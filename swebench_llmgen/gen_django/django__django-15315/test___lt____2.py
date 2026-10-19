import pytest
from django.contrib.auth.models import User
from django.db.models import Field


class CustomField(Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@pytest.mark.parametrize("field1_params, field2_params, expected", [
    ({"verbose_name": "Field A", "name": "field_a", "creation_counter": 1, "model": User},
     {"verbose_name": "Field B", "name": "field_b", "creation_counter": 2, "model": User},
     True),  # Field A < Field B because of lower creation_counter

    ({"verbose_name": "Field B", "name": "field_b", "creation_counter": 1, "model": User},
     {"verbose_name": "Field A", "name": "field_a", "creation_counter": 1, "model": User},
     False),  # Field B >= Field A because creation_counter is equal, compares model (same app label/model name)

    ({"verbose_name": "Field A", "name": "field_a", "creation_counter": 1, "model": User},
     {"verbose_name": "Field C", "name": "field_c", "creation_counter": 1, "model": None},
     False),  # Field A > Field C because Field A has a model and Field C does not

    ({"verbose_name": "Field C", "name": "field_c", "creation_counter": 1, "model": None},
     {"verbose_name": "Field D", "name": "field_d", "creation_counter": 1, "model": User},
     True),  # Field C < Field D because Field C does not have a model

    ({"verbose_name": "Field C", "name": "field_c", "creation_counter": 2, "model": User},
     {"verbose_name": "Field D", "name": "field_d", "creation_counter": 2, "model": User},
     False),  # Should compare models, same values for creation_counter

])
def test_field_lt(field1_params, field2_params, expected):
    field1 = CustomField(**field1_params)
    field2 = CustomField(**field2_params)
    assert (field1 < field2) is expected