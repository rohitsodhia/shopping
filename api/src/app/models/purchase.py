from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models import Receipt


class Purchase(Base):
    __tablename__ = "purchases"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    receipt_id: Mapped[int] = mapped_column(ForeignKey("receipts.id"))
    receipt: Mapped["Receipt"] = relationship(back_populates="purchases")
    _price: Mapped[int] = mapped_column("price", Integer())
    notes: Mapped[str | None] = mapped_column(Text(), nullable=True)

    @hybrid_property
    def price(self):
        return self._price / 100

    @price.inplace.setter
    def set_price(self, value):
        self._price = round(value, 2) * 100
