"""Константы и коды ошибок домена edtech."""

from enum import StrEnum


class ErrorCode(StrEnum):
    """Канонические коды ошибок домена."""

    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"
    BAD_ACTION = "BAD_ACTION"
