import pytest
import enum
from django.utils.functional import Promise

class ChoicesMeta:
    def __new__(metacls, classname, bases, classdict):
        labels = []
        for key in classdict._member_names:
            value = classdict[key]
            if (
                isinstance(value, (list, tuple)) and
                len(value) > 1 and
                isinstance(value[-1], (Promise, str))
            ):
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
    OPTION_ONE = 1, "First Option"
    OPTION_TWO = (2, "Second Option")
    OPTION_THREE = 3

def test_choices_meta_new():
    assert TestChoicesMeta.OPTION_ONE.label == "First Option"
    assert TestChoicesMeta.OPTION_TWO.label == "Second Option"
    assert TestChoicesMeta.OPTION_THREE.label == "Option Three"
    assert TestChoicesMeta._value2label_map_ == {
        1: "First Option",
        2: "Second Option",
        3: "Option Three",
    }
    assert TestChoicesMeta.OPTION_ONE in TestChoicesMeta
    assert TestChoicesMeta.OPTION_TWO in TestChoicesMeta
    assert TestChoicesMeta.OPTION_THREE in TestChoicesMeta
    assert len(TestChoicesMeta) == 3