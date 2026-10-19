import pytest
from django.utils.functional import Promise
from django.contrib.auth.models import User
import enum

class ChoicesMeta(enum.EnumMeta):
    def __new__(metacls, classname, bases, classdict):
        labels = []
        for key in classdict._member_names:
            value = classdict[key]
            if isinstance(value, (list, tuple)) and len(value) > 1 and isinstance(value[-1], (Promise, str)):
                *value, label = value
                value = tuple(value)
            else:
                label = key.replace('_', ' ').title()
            labels.append(label)
            dict.__setitem__(classdict, key, value)
        cls = super().__new__(metacls, classname, bases, classdict)
        cls._value2label_map_ = dict(zip(cls._value2member_map_, labels))
        cls.label = property(lambda self: cls._value2label_map_.get(self.value))
        return enum.unique(cls)

class TestChoicesMeta(enum.Enum, metaclass=ChoicesMeta):
    OPTION_A = 1, "Option A"
    OPTION_B = 2, "Option B"
    OPTION_C = 3, Promise("Option C")

def test_choices_meta_new():
    assert TestChoicesMeta.OPTION_A.value == 1
    assert TestChoicesMeta.OPTION_B.value == 2
    assert TestChoicesMeta.OPTION_C.value == 3
    
    assert TestChoicesMeta.OPTION_A.label == "Option A"
    assert TestChoicesMeta.OPTION_B.label == "Option B"
    assert TestChoicesMeta.OPTION_C.label == "Option C"
    
    assert "OPTION_A" in TestChoicesMeta
    assert "OPTION_B" in TestChoicesMeta
    assert "OPTION_C" in TestChoicesMeta
    
    assert list(TestChoicesMeta.labels()) == ["Option A", "Option B", "Option C"]