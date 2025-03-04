import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models import Store


class Purchase(Base):
    __tablename__ = "purchases"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    _price: Mapped[int] = mapped_column("price", Integer())
    when: Mapped[datetime.datetime] = mapped_column(
        DateTime(), insert_default=func.now()
    )
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"))
    store: Mapped["Store"] = relationship(back_populates="purchases")
    notes: Mapped[str] = mapped_column(Text(), nullable=True)

    @hybrid_property
    def price(self):
        return self._price / 100

    @price.inplace.setter
    def set_price(self, value):
        self._price = round(value, 2) * 100
