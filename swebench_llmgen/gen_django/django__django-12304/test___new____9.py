import enum
from django.utils.functional import Promise
import pytest

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

# Sample Enum class using ChoicesMeta
class UserRoles(enum.Enum, metaclass=ChoicesMeta):
    ADMIN = 1, "Admin"
    MODERATOR = 2, "Moderator"
    USER = 3

def test_choices_meta():
    assert UserRoles.ADMIN.value == (1, "Admin")
    assert UserRoles.MODERATOR.label == "Moderator"
    assert UserRoles(3).label == "User"
    assert UserRoles.USER.label == "User"
    assert UserRoles.ADMIN.label == "Admin"

    # Test resulting labels
    assert UserRoles._value2label_map_[1] == "Admin"
    assert UserRoles._value2label_map_[2] == "Moderator"
    assert UserRoles._value2label_map_[3] == "User"
    
    # Verify unique constraint
    with pytest.raises(ValueError):
        class ConflictingRoles(enum.Enum, metaclass=ChoicesMeta):
            ADMIN = 1, "Duplicate"
            ADMIN_DUPLICATE = 1, "Duplicate"