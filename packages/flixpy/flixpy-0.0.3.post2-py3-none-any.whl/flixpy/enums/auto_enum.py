from enum import Enum


class AutoEnumLower(Enum):
    """Automatically generate lower-case enum value (SOME_ENUM => some_enum)"""

    def _generate_next_value_(name, start, count, last_values) -> str:
        return str(name).lower()


class AutoEnumDashes(Enum):
    """Automatically generate lower-case dashed enum values (SOME_ENUM => some-enum)"""

    def _generate_next_value_(name, start, count, last_values) -> str:
        return str(name).lower().replace("_", "-")
