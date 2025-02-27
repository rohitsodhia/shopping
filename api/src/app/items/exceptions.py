from app.models.item import Item


class ItemAlreadyExists(Exception):
    def __init__(self, item: Item) -> None:
        super().__init__("Item already exists")
        self.item = item
