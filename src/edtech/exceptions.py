"""Специфичные исключения домена edtech."""

from src.edtech import constants


class EdTechError(Exception):
    """Базовое исключение домена с кодом ошибки."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


class NotFoundError(EdTechError):
    """Сущность не найдена (404)."""

    def __init__(self) -> None:
        super().__init__(constants.ErrorCode.NOT_FOUND.value)


class ConflictError(EdTechError):
    """Конфликт состояний, например дублирующая подписка (409)."""

    def __init__(self) -> None:
        super().__init__(constants.ErrorCode.CONFLICT.value)


class BadActionError(EdTechError):
    """Недопустимое значение параметра action (400)."""

    def __init__(self, allowed: list[str]) -> None:
        super().__init__(constants.ErrorCode.BAD_ACTION.value)
        self.allowed = allowed
