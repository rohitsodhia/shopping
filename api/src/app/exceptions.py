class ValidationError(Exception):
    def __init__(self, message: str | None = None) -> None:
        if not message:
            message = "Validation error"
        super().__init__(message)


class NotFound[T](Exception):
    def __init__(self, cls: T) -> None:
        super().__init__(f"{getattr(cls, "__name__")}not found")
        self.cls = cls


class AlreadyExists[T](Exception):
    def __init__(self, cls: T) -> None:
        super().__init__(f"{getattr(cls, "__name__")} already exists")
        self.cls = cls
