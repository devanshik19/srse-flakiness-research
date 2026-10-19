import enum
import pytest
from django.utils.functional import Promise

class ChoicesMeta(enum.EnumMeta):
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
    OPTION_A = 1, "Option A"
    OPTION_B = 2, "Option B"
    OPTION_C = 3,  "Option C"

def test_choices_meta_new_with_labels():
    assert TestChoicesMeta.OPTION_A.label == "Option A"
    assert TestChoicesMeta.OPTION_B.label == "Option B"
    assert TestChoicesMeta.OPTION_C.label == "Option C"

def test_choices_meta_new_without_labels():
    class TestChoicesNoLabels(enum.Enum, metaclass=ChoicesMeta):
        OPTION_X = 1
        OPTION_Y = 2

    assert TestChoicesNoLabels.OPTION_X.label == "Option X"
    assert TestChoicesNoLabels.OPTION_Y.label == "Option Y"

def test_choices_meta_new_with_mixed_labels():
    class TestChoicesMixedLabels(enum.Enum, metaclass=ChoicesMeta):
        OPTION_1 = 1, "First Option"
        OPTION_2 = 2

    assert TestChoicesMixedLabels.OPTION_1.label == "First Option"
    assert TestChoicesMixedLabels.OPTION_2.label == "Option 2"