import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Integer, Text, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models import Store


class Purchase(Base):
    __tablename__ = "purchases"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), nullable=False)
    _price: Mapped[int] = mapped_column("price", Integer(), nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(Date(), insert_default=func.now())
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"), nullable=False)
    store: Mapped["Store"] = relationship(back_populates="purchases")
    notes: Mapped[str] = mapped_column(Text())

    @hybrid_property
    def price(self):
        return self._price / 100

    @price.inplace.setter
    def set_price(self, value):
        self._price = value * 100
