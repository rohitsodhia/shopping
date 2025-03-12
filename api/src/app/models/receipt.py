import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models import Purchase, Store


class Receipt(Base):
    __tablename__ = "receipts"

    id: Mapped[int] = mapped_column(primary_key=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"))
    store: Mapped["Store"] = relationship(back_populates="receipts")
    date: Mapped[datetime.date] = mapped_column(Date())
    purchases: Mapped[list["Purchase"]] = relationship(back_populates="receipt")
    notes: Mapped[str] = mapped_column(Text(), nullable=True)
