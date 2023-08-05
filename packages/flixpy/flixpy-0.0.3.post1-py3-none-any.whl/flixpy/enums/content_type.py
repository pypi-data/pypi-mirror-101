from enum import auto, unique
from flixpy.enums.auto_enum import AutoEnumLower


@unique
class ContentType(AutoEnumLower):
    MOVIE = auto()
    SHOW = auto()
