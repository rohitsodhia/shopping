from app.models.item import Item


class ValidationError(Exception):
    def __init__(self, message: str | None = None) -> None:
        if not message:
            message = "Validation error"
        super().__init__(message)


class ItemAlreadyExists(Exception):
    def __init__(self, item: Item) -> None:
        super().__init__("Item already exists")
        self.item = item
