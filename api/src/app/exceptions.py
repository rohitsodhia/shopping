class ValidationError(Exception):
    def __init__(self, message: str | None = None) -> None:
        if not message:
            message = "Validation error"
        super().__init__(message)


class AlreadyExists(Exception):
    def __init__(self, cls) -> None:
        super().__init__("{type(cls).__name__} already exists")
        self.cls = cls
