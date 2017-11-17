from django.utils.translation import gettext as _

from enum import IntEnum, unique

def django_enum(cls):
    # decorator needed to enable enums in django templates
    cls.do_not_call_in_templates = True
    return cls

@unique
@django_enum
class Status(IntEnum):
    DRAFT = 0
    ACTIVE = 7
    PENDING = 1
    DENIED = 2
    COMPLETED = 3
    ARCHIVED = 4
    HIDDEN = 5
    REMOVED = 6


@unique
@django_enum
class PersonGroupType(IntEnum):
    DEFAULT = 0
    TEACHER = 1
    STUDENT = 2
    