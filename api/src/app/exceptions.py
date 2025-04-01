class ValidationError(Exception):
    def __init__(self, message: str | None = None) -> None:
        if not message:
            message = "Validation error"
        super().__init__(message)


class NotFound[T](Exception):
    def __init__(self, cls: T) -> None:
        if isinstance(cls, type):
            cls_name = cls.__name__
        else:
            cls_name = type(cls).__name__
        super().__init__(f"{cls_name} not found")
        self.cls = cls


class AlreadyExists[T](Exception):
    def __init__(self, cls: T) -> None:
        if isinstance(cls, type):
            cls_name = cls.__name__
        else:
            cls_name = type(cls).__name__
        super().__init__(f"{cls_name} already exists")
        self.cls = cls
